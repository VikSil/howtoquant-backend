books_select_all = '''
    SELECT b.id, b.name, b.external_name, am.method_name AS accounting_method, ccy.iso AS base_currency, acc.account_name AS broker_account, o.short_name as fund_name FROM accounting_book AS b
    LEFT JOIN classifiers_accounting_method AS am ON b.accounting_method_id = am.id
    LEFT JOIN classifiers_currency AS ccy ON b.base_ccy_id = ccy.id
    LEFT JOIN accounting_broker_account AS acc ON b.default_account_id = acc.id
    LEFT JOIN staticdata_organization AS o ON b.fund_org_id = o.id 
'''

books_select_all_names = '''
    SELECT b.name FROM accounting_book AS b
'''

cash_positions_select_all_where_date = '''
    SELECT cl.date, cl.position_id, cl.quantity, ccy.ISO AS ccy, b.name AS book, s.name AS strategy, bacc.account_name as account
    FROM accounting_cash_ladder AS cl
    LEFT JOIN accounting_cash_position AS cp ON cl.position_id = cp.id
    LEFT JOIN classifiers_currency AS ccy ON cp.ccy_id = ccy.id
    LEFT JOIN accounting_book AS b ON cp.book_id = b.id
    LEFT JOIN accounting_broker_account AS bacc ON cp.account_Id = bacc.id
    LEFT JOIN accounting_strategy AS s ON cp.strategy_id = s.id
    WHERE cl.date >= %s AND cl.date <= %s
'''

instrument_positions_select_all_where_date = '''
    SELECT al.date, al.position_id, al.quantity, ticker.code, b.name AS book, s.name AS strategy, bacc.account_name as account
    FROM accounting_asset_ladder AS al
    LEFT JOIN accounting_instrument_position AS ip ON al.position_id = ip.id
    LEFT JOIN staticdata_instrument AS inst ON ip.instrument_id = inst.id
    LEFT JOIN staticdata_identifier AS ticker ON ticker.instrument_id = inst.id 
    LEFT JOIN accounting_book AS b ON ip.book_id = b.id
    LEFT JOIN accounting_broker_account AS bacc ON ip.account_Id = bacc.id
    LEFT JOIN accounting_strategy AS s ON ip.strategy_id = s.id
    WHERE ticker.identifier_type_id = 6
    AND al.date >= %s AND al.date <= %s
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

strategies_select_all_names = '''
    SELECT s.name FROM accounting_strategy AS s
'''

trades_select_all = '''
    SELECT t.id, ts.name AS status, t.bs_indicator AS "B/S", t.quantity AS qty, i.short_name AS inst,
    t.price, ccy_t.ISO AS ccy, t.gross_consideration AS consid, DATE_FORMAT(t.trade_datetime, '%Y-%m-%d %H:%i:%s') AS trade_dt, DATE(t.settlement_date) AS settle_dt,
    b.name AS book, s.name AS strat, acc.account_name AS acct, cpty.short_name AS cpty
    FROM accounting_trade AS t
    LEFT JOIN classifiers_trade_status AS ts ON t.trade_status_id = ts.id
    LEFT JOIN staticdata_instrument AS i ON t.instrument_id = i.id
    LEFT JOIN classifiers_currency AS ccy_t ON t.ccy_id = ccy_t.id
    LEFT JOIN accounting_book AS b ON t.book_id = b.id
    LEFT JOIN accounting_strategy s ON t.strategy_id = s.id
    LEFT JOIN accounting_broker_account acc ON t.account_id = acc.id
    LEFT JOIN staticdata_organization as cpty ON t.counterparty_id = cpty.id    
'''


trades_select_where_id = '''
    SELECT t.id, ts.name AS status, t.bs_indicator AS "B/S_direction", t.quantity, i.short_name AS instrument,
    t.price, ccy_t.ISO AS trade_currency, t.gross_consideration, DATE(t.trade_datetime) AS trade_date,
    TIME(t.trade_datetime) AS trade_time, DATE(t.settlement_date) AS settlement_date, ccy_s.ISO as settlement_currency, t.trade_settlement_xrate AS "Trade/Settlement xrate", t.settlement_base_xrate AS "Settlement/Base xrate",
    b.name AS book, s.name AS strategy, acc.account_name AS PB_account, cpty.short_name AS counterparty, DATE(t.created) AS input_date, TIME(t.created) AS input_time
    FROM accounting_trade AS t
    LEFT JOIN classifiers_trade_status AS ts ON t.trade_status_id = ts.id
    LEFT JOIN staticdata_instrument AS i ON t.instrument_id = i.id
    LEFT JOIN classifiers_currency AS ccy_t ON t.ccy_id = ccy_t.id
    LEFT JOIN accounting_book AS b ON t.book_id = b.id
    LEFT JOIN accounting_strategy s ON t.strategy_id = s.id
    LEFT JOIN accounting_broker_account acc ON t.account_id = acc.id
    LEFT JOIN classifiers_currency AS ccy_s ON t.settlement_ccy_id = ccy_s.id
    LEFT JOIN staticdata_organization as cpty ON t.counterparty_id = cpty.id
    WHERE t.id = %s 
'''
