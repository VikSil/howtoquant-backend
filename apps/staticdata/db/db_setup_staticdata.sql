alter table staticdata_organization modify column created datetime default CURRENT_TIMESTAMP;
alter table staticdata_organization modify column updated datetime default CURRENT_TIMESTAMP;

alter table staticdata_instrument modify column created datetime default CURRENT_TIMESTAMP;
alter table staticdata_instrument modify column updated datetime default CURRENT_TIMESTAMP;

alter table staticdata_identifier modify column created datetime default CURRENT_TIMESTAMP;
alter table staticdata_identifier modify column updated datetime default CURRENT_TIMESTAMP;

alter table staticdata_equity modify column created datetime default CURRENT_TIMESTAMP;
alter table staticdata_equity modify column updated datetime default CURRENT_TIMESTAMP;
alter table staticdata_equity alter dividend_frequency set default 0;