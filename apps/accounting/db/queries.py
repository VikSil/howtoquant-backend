books_select_all = '''
    SELECT b.id, b.name, b.external_name, am.method_name AS accounting_method, ccy.iso AS base_currency, acc.account_name AS broker_account, o.short_name as fund_name FROM accounting_book AS b
    LEFT JOIN classifiers_accounting_method AS am ON b.accounting_method_id = am.id
    LEFT JOIN classifiers_currency AS ccy ON b.base_ccy_id = ccy.id
    LEFT JOIN accounting_broker_account AS acc ON b.default_account_id = acc.id
    LEFT JOIN staticdata_organization AS o ON b.fund_org_id = o.id 
'''

pbaccounts_select_all = '''
    SELECT acc.id, acc.account_name, acc.external_name, b.short_name AS broker, f.short_name AS fund,
    CASE
      WHEN acc.cash_account = 0 THEN 'Regular Account'
      WHEN acc.cash_account = 1 THEN 'Cash Account'
    END AS account_type
    FROM accounting_broker_account AS acc
    LEFT JOIN staticdata_organization AS b ON acc.broker_org_id = b.id
    LEFT JOIN staticdata_organization AS f ON acc.fund_org_id = f.id
'''

pbaccounts_select_all_names = '''
    SELECT account_name from accounting_broker_account AS acc
    LEFT JOIN staticdata_organization AS o ON acc.fund_org_id = o.id
    LEFT JOIN classifiers_organization_type AS ot ON o.org_type_id = ot.id
    WHERE ot.type_name in ('Fund', 'Headquarters')
    AND o.short_name = %s    
'''


strategies_select_all = '''
    SELECT s.id, s.name, s.description FROM accounting_strategy AS s
'''

trades_select_all = '''
    SELECT t.id, ts.name, t.bs_indicator AS direction, t.quantity, i.short_name AS instrument,
    t.price, ccy_t.ISO AS ccy, t.gross_consideration, t.trade_datetime, t.settlement_date, ccy_s.ISO as settlement_ccy, t.trade_settlement_xrate,
    b.name AS book, s.name AS strategy, acc.account_name AS account, cpty.short_name AS counterparty
    FROM accounting_trade AS t
    LEFT JOIN classifiers_trade_status AS ts ON t.trade_status_id = ts.id
    LEFT JOIN staticdata_instrument AS i ON t.instrument_id = i.id
    LEFT JOIN classifiers_currency AS ccy_t ON t.ccy_id = ccy_t.id
    LEFT JOIN accounting_book AS b ON t.book_id = b.id
    LEFT JOIN accounting_strategy s ON t.strategy_id = s.id
    LEFT JOIN accounting_broker_account acc ON t.account_id = acc.id
    LEFT JOIN classifiers_currency AS ccy_s ON t.settlement_ccy_id = ccy_s.id
    LEFT JOIN staticdata_organization as cpty ON t.counterparty_id = cpty.id    
'''
