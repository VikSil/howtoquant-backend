# Trade processing workflow

This document details how trades are processed into the system.

## Booking

Trades can be booked either via GUI or by sending in an API request.

<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/minimal_POST_trade_body.png" alt="Minimal POST trade body"/>
</p>

**Endpoint**: /accounting/api/trades

**View**: trades

**Tables**:

* ACCOUNTING_TRADE - Captures the data submitted via API
<p align = "center">
<img height ="300" src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/accounting_trade_record.png" alt="Trade record"/>
</p>

* CONFIG_MSG_QUEUE - A record for each trade signalling to FLOW_BOOKER
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/FLOW_BOOKER_N_message.png" alt="New message to FlowBooker service"/>
</p>


## FlowBooker processing

### New messages

**Input msg_queue flag**: N

**Processing**: None

**Output**: CONFIG_MSG_QUEUE 

* A new record for each trade signaling to PositionManager (to check if position exists)
    
    * arg1 - ACCOUNTING_TRADE.ID
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/POS_MANAGER_N_message.png" alt="New message to PositionManager service"/>
</p>

* Amended records to self, flag N --> P
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/FLOW_BOOKER_P_message.png" alt="Message awaiting PositionManager"/>
</p>


### Mesages with existing position

**Input msg_queue flag**: F

**Processing**:

* Check if record for instrument position flow already exists in ACCOUNTING_ASSET_FLOW (amended trade), if not (new trade) then create a new record

    * PRICE is denominated in trade ccy
    * CCY_ID is trade ccy
    * XRATE is trade-base xrate, calculated as ACCOUNTING_TRADE.TRADE_SETTLEMENT_XRATE * ACCOUNTING_TRADE.SETTLEMENT_BASE_XRATE
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/accounting_asset_flow_record.png" alt="Instrument flow record"/>
</p>

* Check if record for settlement ccy flow already exists in ACCOUNTING_ASSET_FLOW, if not then create a new record
    * QUANTITY is gross consideration adjusted for direction
    * PRICE is in settlement ccy (trade price * trade-settlement xrate)
    * XRATE is settlement-base xrate
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/accounting_asset_flow_cash_record.png" alt="Cash flow record"/>
</p>

*N.B. ACCOUNTING_ASSET_FLOW has Generic Foreign Key, hence source_id in SQL points to DJANGO_CONTENT_TYPE, **not** ACCOUNTING_TRADE. Instrument flows and cash flows are distinguished by ASSET_FLOW_TYPE_ID column (1 - instrument, 2- cash)*

**Output**: CONFIG_MSG_QUEUE

* Amended records to self
    * Successfuly processed flag N --> X
    * Failed processing flag N --> Z

* A new record for each trade signaling to AssetManager to recalculate asset ladder
    
    * arg1 - ACCOUNTING_INSTRUMENT_POSITION.ID
    * arg2 - ACCOUNTING_TRADE.TRADE_DATETIME
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/ASSET_MANAGER_N_message.png" alt="New message to PositionManager service"/>
</p>

* A new record for each trade signaling to CashManager to recalculate cash ladder
    
    * arg3 - ACCOUNTING_CASH_POSITION.ID
    * arg4 - ACCOUNTING_TRADE.SETTLEMENT_DATE
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/CASH_MANAGER_N_message.png" alt="New message to PositionManager service"/>
</p>

## PositionManager processing

### New messages

**Input msg_queue flag**: N

**Processing**:

* Check if record already exists in ACCOUNTING_INSTRUMENT_POSITION, if not then create a new record
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/accounting_instrument_position_record.png" alt="Instrument position record"/>
</p>

* Check if trade ccy record for this instrument position already exists in ACCOUNTING_CASH_POSITION, if not then create a new record

* Check if settlement ccy record for this instrument position already exists in ACCOUNTING_CASH_POSITION, if not then create a new record
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/accounting_cash_position_record.png" alt="Cash position record"/>
</p>

**Output**: CONFIG_MSG_QUEUE 

* Amended records to self
    * Successfuly processed flag N --> X
    * Failed processing flag N --> Z

* Amend originating records to FLOW_BOOKER
    * Failed processing 
        * flag P --> Y
    * Successfuly processed
        * arg1 - ACCOUNTING.INSTRUMENT_POSITION.ID
        * arg2 - ACCOUNTING.CASH_POSITION.ID for trade ccy
        * arg3 -  ACCOUNTING.CASH_POSITION.ID for settlement ccy
        * flag P --> F
 <p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/FLOW_BOOKER_F_message.png" alt="Message awaiting FlowBooker"/>
</p>   

