DROP TABLE accounting_position_snapshot;
DROP TABLE accounting_fifo_pnl;
DROP TABLE accounting_weighted_pnl;
DROP TABLE accounting_asset_ladder;
DROP TABLE accounting_cash_ladder;
DROP TABLE accounting_asset_flow;
DROP TABLE accounting_accrual_ladder;
DROP TABLE accounting_cash_position;
DROP TABLE accounting_instrument_position;
DROP TABLE accounting_trade;
DROP TABLE accounting_strategy;

source E:\05_Ultimate_Brain\Finance_Skills\HowToQuant\backend\apps\marketdata\db\drop_marketdata.sql

DROP TABLE accounting_book;
DROP TABLE accounting_broker_account;

source E:\05_Ultimate_Brain\Finance_Skills\HowToQuant\backend\apps\staticdata\db\drop_staticdata.sql
source E:\05_Ultimate_Brain\Finance_Skills\HowToQuant\backend\apps\classifiers\db\drop_classifiers.sql

DELETE FROM django_migrations WHERE app in ('accounting','staticdata', 'classifiers', 'marketdata');







