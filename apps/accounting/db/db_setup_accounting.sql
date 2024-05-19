alter table accounting_position_snapshot modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_position_snapshot modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_fifo_pnl modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_fifo_pnl modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_weighted_pnl modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_weighted_pnl modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_asset_ladder modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_asset_ladder modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_cash_ladder modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_cash_ladder modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_asset_flow modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_asset_flow modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_accrual_ladder modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_accrual_ladder modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_cash_position modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_cash_position modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_instrument_position modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_instrument_position modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_trade modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_trade modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_strategy modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_strategy modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_book modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_book modify column updated datetime default CURRENT_TIMESTAMP;

alter table accounting_broker_account modify column created datetime default CURRENT_TIMESTAMP;
alter table accounting_broker_account modify column updated datetime default CURRENT_TIMESTAMP;

