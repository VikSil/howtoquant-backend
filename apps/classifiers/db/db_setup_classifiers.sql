alter table classifiers_identifier_type modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_identifier_type modify column update_date datetime default CURRENT_TIMESTAMP;

alter table classifiers_instrument_class modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_instrument_class modify column update_date datetime default CURRENT_TIMESTAMP;

alter table classifiers_currency modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_currency modify column update_date datetime default CURRENT_TIMESTAMP;

alter table classifiers_country modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_country modify column update_date datetime default CURRENT_TIMESTAMP;

alter table classifiers_organization_type modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_organization_type modify column update_date datetime default CURRENT_TIMESTAMP;

alter table classifiers_industry_sector modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_industry_sector modify column update_date datetime default CURRENT_TIMESTAMP;

alter table classifiers_industry_subsector modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_industry_subsector modify column update_date datetime default CURRENT_TIMESTAMP;

alter table classifiers_market_data_source modify column created_date datetime default CURRENT_TIMESTAMP;
alter table classifiers_market_data_source modify column update_date datetime default CURRENT_TIMESTAMP;