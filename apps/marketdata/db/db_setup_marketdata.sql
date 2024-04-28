alter table marketdata_value_field modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_field modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_spec modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_spec modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_value_field_to_spec modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_value_field_to_spec modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_download modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_download modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_download_tickers modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_download_tickers modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_download_data modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_download_data modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_price_ladder modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_price_ladder modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_xrate_ladder modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_xrate_ladder modify column update_date datetime default CURRENT_TIMESTAMP;

alter table marketdata_analytics_ladder modify column created_date datetime default CURRENT_TIMESTAMP;
alter table marketdata_analytics_ladder modify column update_date datetime default CURRENT_TIMESTAMP;
