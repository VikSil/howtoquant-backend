alter table staticdata_organization modify column created_date datetime default CURRENT_TIMESTAMP;
alter table staticdata_organization modify column update_date datetime default CURRENT_TIMESTAMP;

alter table staticdata_instrument modify column created_date datetime default CURRENT_TIMESTAMP;
alter table staticdata_instrument modify column update_date datetime default CURRENT_TIMESTAMP;

alter table staticdata_identifier modify column created_date datetime default CURRENT_TIMESTAMP;
alter table staticdata_identifier modify column update_date datetime default CURRENT_TIMESTAMP;

alter table staticdata_equity modify column created_date datetime default CURRENT_TIMESTAMP;
alter table staticdata_equity modify column update_date datetime default CURRENT_TIMESTAMP;
alter table staticdata_equity alter dividend_frequency set default 0;