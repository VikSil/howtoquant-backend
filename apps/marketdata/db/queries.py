download_data_select_prices = 'CALL get_download_prices(%s)'

price_ladder_select_all = '''
    SELECT pl.id, pl.value_date, pl.bid_price, pl.ask_price, inst.short_name AS instrument, vf.description AS value_field, mds.source_name AS source
    FROM marketdata_price_ladder AS pl
    LEFT JOIN staticdata_instrument AS inst ON pl.instrument_id = inst.id
    LEFT JOIN marketdata_value_field AS vf ON pl.value_field_id = vf.id
    LEFT JOIN classifiers_market_data_source as mds ON vf.market_data_source_id= mds.id
    WHERE pl.owner_org_id = 1;
'''

save_download_prices_proc = 'save_download_prices'
