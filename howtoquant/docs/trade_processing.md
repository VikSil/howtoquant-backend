# Trade processing workflow

This document details how trades are processed into the system.

## Booking

Trades can be booked either via GUI or by sending in an API request.

<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/minimal_POST_tade_body.png" alt="Minimal POST trade body"/>
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
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/FLOW_BOOKER_N_Message.png" alt="New message to FlowBooker service"/>
</p>


## FlowBooker processing

### New messages

**Input msg_queue flag**: N

**Processing**: None

**Output**: CONFIG_MSG_QUEUE 

* A new record for each trade signalling to PositionManager (to check if position exists)
    
    * arg1 - ACCOUNTING_TRADE.ID
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/POS_MANAGER_N_Message.png" alt="New message to PositionManager service"/>
</p>

* Amended records to self, flag N --> P
<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/FLOW_BOOKER_P_Message.png" alt="Message awaiting PositionManager"/>
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

