# Trade processing workflow

## Services and MSG_QUEUE
Trade processing is carried out by several Services that are periodically run as cron jobs.
The services are:

* FlowBooker
* PositionManager
* CashManager
* AssetManager

These services communicate with each other by placing messages into CONFIG_MSG_QUEUE table. At each run, each service check the message queue for messages addressed to itself and carries out processing in accordance with the messages found on queue. The processing is described for each service in detail below.

Each message on the queue has a FLAG field that indicates the stage of processing of that message.
There are two types of flags - generic and service specific. Generic flags are shared between services and have the same meaning on all messages. Service specific flags 'belong' to a specific service. If a message is flagged with a service specific flag, it means that the workflow control has been handed off to that service. If the flagged service and CONFIG_MSG_QUEUE.PROCESS are the same, it means that workflow control has been handed back to that service. 

**Generic flag values**

* N - New - Will be picked up for processing by the designated service 
* X - Terminated - work on the message complete
* Y - Downstream failure - error occured during downstream processing
* Z - Failure - error occured during processing by the designated service

**Service specific flag values**

* F - Flow processing - workflow awaiting FlowBooker
* P - Position processing - workflow awaiting PositionManager



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


## Cash Manager procesing

**Input msg_queue flag**: N

**Processing**: For each cash position

* Find the message on queue with the oldest settlement date
* Retrieve all cash flows from ACCOUNTING_ASSET_FLOW for dates later or equal to that settlement date
* Forward fill dataframe with cumulative flow quantity for each date in the range from the settlement date or last ladder date, whichever is earlier, to the latest flow date
* Check if any records exist in ACCOUNTING_CASH_LADDER
    * if no records exist, insert flow dataframe into ACCOUNTING_CASH_LADDER
    * if records exist
        * check if there are records in ACCOUNTING_CASH_LADDER earlier than the settlement date
            * if there are earlier records, update each quantity in flows dataframe by adding the quantity from ACCOUNTING_CASH_LADDER on the day before settlement date. Update existing records in ACCOUNTING_CASH_LADDER with the new quantities from flows dataframe
            * if there are no earlier records find the earliest date in ACCOUNTING_CASH_LADDER. Partition flows dataframe in two parts - before and on-and-after earliest ladder date. Insert the before part into the database. Use the on-and-after part to update the existing records.
        * check if the latest date in ACCOUNTING_CASH_LADDER is less than the latest date in flows dataframe (projected settlements). If there are, select rows from flows dataframe with dates greater than the latest ladder date and insert into the database.

<p align = "center">
<img src="https://github.com/VikSil/howtoquant-backend/blob/trunk/howtoquant/docs/img/accounting_cash_ladder_records.png" alt="Cash ladder records"/>
</p>

**Output**: CONFIG_MSG_QUEUE 

* Amended records to self
    * Successfuly processed flag N --> X
    * Failed processing flag N --> Z 
   