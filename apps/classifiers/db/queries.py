accounting_method_select_all_names = 'SELECT method_name FROM classifiers_accounting_method'

country_select_all = 'SELECT * FROM classifiers_country WHERE active = %s'
country_select_all_names = 'SELECT short_name FROM classifiers_country WHERE active = %s'
country_set_active_where_iso2 = 'UPDATE classifiers_country SET active = 1 WHERE ISO2 = %s'

currency_select_all = 'SELECT * FROM classifiers_currency WHERE active = %s'
currency_select_all_codes = 'SELECT iso FROM classifiers_currency WHERE active = %s'
currency_set_active = 'UPDATE classifiers_currency SET active = 1 WHERE ISO = %s'

identifier_type_select_specified = 'SELECT * FROM classifiers_identifier_type WHERE id > 4'

industry_sector_select_all = 'SELECT * FROM classifiers_industry_sector'
industry_sector_select_all_names = 'SELECT sector_name FROM classifiers_industry_sector'

industry_subsector_select_all = 'SELECT * FROM classifiers_industry_subsector'
industry_subsector_select_all_names = 'SELECT subsector_name FROM classifiers_industry_subsector'

instrument_class_select_all_names = 'SELECT instrument_class FROM classifiers_instrument_class  WHERE id > 4'
instrument_class_select_specified = 'SELECT * FROM classifiers_instrument_class WHERE id > 4'

organization_type_select_all = 'SELECT * FROM classifiers_organization_type'
