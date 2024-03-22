identifier_type_queries = {
    'select_all': "SELECT * FROM staticdata_identifier_type",

}

identifier_type_select_all = "SELECT * FROM staticdata_identifier_type"

# this is invoked by cursor.execute(identifier_type_select_where_id, [s_variable]) 
identifier_type_select_where_id = "SELECT * FROM staticdata_identifier_type WHERE id = %s"
