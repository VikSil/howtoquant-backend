alter table classifiers_identifier_type modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_identifier_type modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_instrument_class modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_instrument_class modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_currency modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_currency modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_country modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_country modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_organization_type modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_organization_type modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_industry_sector modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_industry_sector modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_industry_subsector modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_industry_subsector modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_market_data_source modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_market_data_source modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_accounting_method modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_accounting_method modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_trade_status modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_trade_status modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_position_type modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_position_type modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_accrual_type modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_accrual_type modify column updated datetime default CURRENT_TIMESTAMP;

alter table classifiers_asset_flow_type modify column created datetime default CURRENT_TIMESTAMP;
alter table classifiers_asset_flow_type modify column updated datetime default CURRENT_TIMESTAMP;