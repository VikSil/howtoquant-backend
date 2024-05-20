delete from staticdata_identifier;
delete from staticdata_equity;
delete from staticdata_instrument;
delete from staticdata_organization WHERE owner_org_id in (1,9);
delete from staticdata_organization;
