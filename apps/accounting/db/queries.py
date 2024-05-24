books_select_all = '''
    SELECT b.id, b.name, b.external_name, am.method_name AS accounting_method, ccy.iso AS base_currency, acc.account_name AS broker_account, o.short_name as fund_name FROM accounting_book AS b
    LEFT JOIN classifiers_accounting_method AS am ON b.accounting_method_id = am.id
    LEFT JOIN classifiers_currency AS ccy ON b.base_ccy_id = ccy.id
    LEFT JOIN accounting_broker_account AS acc ON b.default_account_id = acc.id
    LEFT JOIN staticdata_organization AS o ON b.fund_org_id = o.id 
'''

strategies_select_all = '''
    SELECT s.id, s.name, s.description FROM accounting_strategy AS s
'''

pbaccounts_select_all = '''
    SELECT acc.id, acc.account_name, acc.external_name, b.short_name as broker, f.short_name as fund,
    CASE
      WHEN acc.cash_account = 0 THEN 'Regular Account'
      WHEN acc.cash_account = 1 THEN 'Cash Account'
    END AS account_type
    FROM accounting_broker_account AS acc
    LEFT JOIN staticdata_organization AS b ON acc.broker_org_id = b.id
    LEFT JOIN staticdata_organization AS f ON acc.fund_org_id = f.id
'''
