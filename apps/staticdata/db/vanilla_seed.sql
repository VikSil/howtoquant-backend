INSERT INTO staticdata_identifier_type VALUES
(1, 'ISIN'),
(2, 'BBG Ticker'),
(3, 'Sedol'),
(4, 'RIC'),
(5, 'Internal');
(6, 'BBG Exchange Code');

INSERT INTO staticdata_instrument_class VALUES
(1, 'Equity', 'Simple Stock');

INSERT INTO staticdata_equity VALUES
(1, 'Tesla', 1),
(2, 'Beyond Meat', 1),
(3, 'Linesata Services', 1);

INSERT INTO staticdata_identifier VALUES
(1, 'TSLA', 1, 2, 4),
(2, 'BYND', 2, 2, 4),
(3, 'LIN', 3, 2, 4);
