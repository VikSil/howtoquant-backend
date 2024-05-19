alter table marketdata_value_field modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_field modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_spec modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_spec modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_field_to_spec modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_field_to_spec modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_scheme_pref modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_scheme_pref modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_scheme modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_scheme modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_scheme_order modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_scheme_order modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_scheme_rule modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_scheme_rule modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_download modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_download modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_download_tickers modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_download_tickers modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_download_data modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_download_data modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_price_ladder modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_price_ladder modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_xrate_ladder modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_xrate_ladder modify column updated datetime default CURRENT_TIMESTAMP;

alter table marketdata_analytics_ladder modify column created datetime default CURRENT_TIMESTAMP;
alter table marketdata_analytics_ladder modify column updated datetime default CURRENT_TIMESTAMP;
