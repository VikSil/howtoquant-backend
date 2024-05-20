INSERT INTO accounting_broker_account (id, account_name, external_name, cash_account, broker_org_id, fund_org_id) VALUES
(1,'Morgan Sachs Account','MS000000010',0,11,10),
(2,'Morgan Sachs Cash Account','MS000000011',0,11,10);

INSERT INTO accounting_book (id, name, external_name, accounting_method_id, base_ccy_id, default_account_id, fund_org_id) VALUES
(1, 'Long Short', 'SP MF LS', 1, 5,1,10),
(2, 'Global Macro', 'SP MF GM', 2, 5, 1, 10);

INSERT INTO accounting_strategy (id, name, description, owner_org_id) VALUES
(1, 'Long Only', 'Long Only Strategy',9),
(2, 'China Short', 'China is Sadly Going Away',9),
(3, 'Short Sell', 'Opportunistic Shorts',9),
(4, 'Africa', 'Africa Investment Strategy',9);
