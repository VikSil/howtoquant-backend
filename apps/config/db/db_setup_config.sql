alter table config_msg_queue modify column created datetime default CURRENT_TIMESTAMP;
alter table config_msg_queue modify column updated datetime default CURRENT_TIMESTAMP;