equities_select_all = '''
    select i.id, i.name, i.short_name, org.short_name as issuer, ccy.ISO as base_ccy, ctry.short_name as domicile from staticdata_equity as eq
    JOIN staticdata_instrument as i ON eq.instrument_id = i.id 
    JOIN classifiers_currency as ccy ON i.base_ccy_id = ccy.id 
    JOIN classifiers_country as ctry ON i.domicile_id = ctry.id
    JOIN staticdata_organization as org ON i.issuer_id = org.id
    WHERE i.owner_org_id = 1
    ;
'''

identifier_type_select_all = "SELECT * FROM staticdata_identifier_type"

# this is invoked by cursor.execute(identifier_type_select_where_id, [s_variable])
# multiple variables are all referred to as %s and replced with values from the list in order
identifier_type_select_where_id = 'SELECT * FROM staticdata_identifier_type WHERE id = %s'

identifier_type_delete_where_id = 'DELETE FROM staticdata_identifier_type WHERE id = %s'

identifiers_select_all = '''
    SELECT i.id, i.code, itype.type_name AS type, inst.id AS inst_id, inst.short_name as instrument FROM staticdata_identifier AS i
    JOIN classifiers_identifier_type AS itype ON i.identifier_type_id = itype.id
    JOIN staticdata_instrument AS inst ON i.instrument_id = inst.id
    WHERE inst.owner_org_id = 1
    ;
'''

identifiers_select_all_codes = 'SELECT code FROM staticdata_identifier'

instruments_select_where_id = '''
    SELECT i.id, o.short_name AS issuer, ic.instrument_class, c.short_name AS domicile, ccy.ISO AS ccy, isec.sector_name, t.code AS ticker, tt.type_name AS ticker_type  FROM staticdata_instrument AS i
    LEFT JOIN classifiers_currency AS ccy on i.base_ccy_id = ccy.id
    LEFT JOIN classifiers_country as c on i.domicile_id = c.id
    LEFT JOIN classifiers_instrument_class As ic on i.instrument_class_id = ic.id
    LEFT JOIN staticdata_equity AS e ON i.id = e.instrument_id
    LEFT JOIN classifiers_industry_sector isec ON e.sector_id = isec.id
    LEFT JOIN staticdata_organization AS o ON i.issuer_id = o.id
    LEFT JOIN staticdata_identifier AS t ON i.id = t.instrument_id
    LEFT JOIN classifiers_identifier_type AS tt ON t.identifier_type_id = tt.id
    WHERE i.id = %s
'''

organization_select_all = '''
    SELECT o.id, o.short_name, o.long_name, o.description, oo.short_name as parent FROM staticdata_organization o
    LEFT JOIN classifiers_organization_type AS ot ON o.org_type_id = ot.id
    LEFT JOIN staticdata_organization AS oo ON o.owner_org_id = oo.id
'''

organizations_select_all_broker_names = '''
    SELECT short_name FROM staticdata_organization
    WHERE org_type_id in (
	    SELECT id FROM classifiers_organization_type
        WHERE type_name in ('Prime Broker'))
'''

organizations_select_all_fund_names = '''
    SELECT short_name FROM staticdata_organization
    WHERE org_type_id in (
	    SELECT id FROM classifiers_organization_type
        WHERE type_name in ('Headquarters', 'Fund'))
'''

organizations_select_all_issuer_names = '''
    SELECT short_name FROM staticdata_organization
    WHERE org_type_id in (
	    SELECT id FROM classifiers_organization_type
        WHERE type_name in ('Issuer'))
'''

organizations_select_all_parent_org_names = '''
    SELECT short_name FROM staticdata_organization
    WHERE org_type_id in (
	    SELECT id FROM classifiers_organization_type
        WHERE type_name in ('Headquarters', 'Public'))
'''

organization_select_where_type = '''
    SELECT o.id, o.short_name, o.long_name, o.description, oo.short_name as parent FROM staticdata_organization o
    LEFT JOIN classifiers_organization_type AS ot ON o.org_type_id = ot.id
    LEFT JOIN staticdata_organization AS oo ON o.owner_org_id = oo.id
    WHERE ot.type_name = %s
'''

ticker_select_where_code = 'SELECT instrument_id FROM staticdata_identifier WHERE code = %s'
