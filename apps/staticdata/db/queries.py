identifier_type_queries = {
    'select_all': "SELECT * FROM staticdata_identifier_type",

}

identifier_type_select_all = "SELECT * FROM staticdata_identifier_type"

# this is invoked by cursor.execute(identifier_type_select_where_id, [s_variable])
# multiple variables are all referred to as %s and replced with values from the list in order
identifier_type_select_where_id = "SELECT * FROM staticdata_identifier_type WHERE id = %s"

identifier_type_delete_where_id  = "DELETE FROM staticdata_identifier_type WHERE id = %s"

equities_with_inst_type_select_all = '''SELECT eq.id, eq.name, inst_class.instrument_type, inst_class.instrument_class
    FROM staticdata_equity eq 
    JOIN staticdata_instrument_class inst_class
    ON eq.instrument_class_id = inst_class.id
    '''

equities_select_all = '''
    select i.id, i.name, i.short_name, org.short_name as issuer, ccy.ISO as base_ccy, ctry.short_name as domicile from staticdata_equity as eq
    JOIN staticdata_instrument as i ON eq.instrument_id_id = i.id 
    JOIN classifiers_currency as ccy ON i.base_ccy_id_id = ccy.id 
    JOIN classifiers_country as ctry ON i.domicile_id_id = ctry.id
    JOIN staticdata_organization as org ON i.issuer_id_id = org.id
    WHERE i.owner_org_id_id = 1
    ;
'''
