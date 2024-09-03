# Release notes

* Microservices added:
    * FlowBooker - coordinates the workflow between other services
    * PositionManager - handles position creation
    * CashManager - handles cash ladder
    * AssetManager - handles asset ladder
    * Rollforward - carries ladders onto a new business day 
* Config app added with msg_queue for communication between services
* GET endpoints implemented for:
     * accounting app: trade, cash_ladder, asset_ladder, book names, strategy names
     * classifiers app: trade_status
     * staticdata app: counteroarty organization names
* POST endpoints implemented for:
     * accounting app: trade
* Updates to trade, value_schema, value_scheme_rule value_spec, value_order models in accounting app
* Data added in classifiers and staticdata MySQL seeding scripts
* Logging added
* Documentation added:
    * Trade processing detailing microservices and processing workflow
    * Deployment manual