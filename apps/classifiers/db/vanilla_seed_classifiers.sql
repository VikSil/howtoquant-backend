INSERT INTO classifiers_identifier_type VALUES
(1, 'ISIN'),
(2, 'BBG Ticker'),
(3, 'Sedol'),
(4, 'RIC'),
(5, 'Internal Ticker'),
(6, 'BBG Exchange Code');

INSERT INTO classifiers_instrument_class VALUES
(1, 'Equity', 'Simple Stock');

INSERT INTO classifiers_currency VALUES
(1, 'United States Dollar', 'Cent', 100, 'USD'),
(2, 'Euro', 'Cent', 100, 'EUR'),
(3, 'Pound sterling', 'Pence', 100, 'GBP'),
(4, 'Swiss frank', 'Rappen/Centime', 1000, 'CHF'),
(5, 'Japanese yen', '', 0, 'JPY');

INSERT INTO classifiers_country VALUES
(1, 'The United States of America', 'USA', 'US', 'USA', 1),
(2, 'The Federal Republic of Germany', 'Germany', 'DE', 'DEU' , 2),
(3, 'The United Kingdom of Great Britain and Northern Ireland', 'UK', 'GB', 'GBR' , 3),
(4, 'The Swiss Confederation', 'Switzerland', 'CH', 'CHE' , 4),
(5, 'Japan', 'Japan', 'JP', 'JPN' , 5);

INSERT INTO classifiers_organization_type VALUES
(1, 'Internal'),
(2, 'Headquarters'),
(3, 'Issuer');

INSERT INTO classifiers_industry_sector VALUES
(1, 'Automotive'),
(2, 'Telecommunications');

INSERT INTO classifiers_industry_subsector VALUES
(1, 'Automotive', 1),
(2, 'Telecommunications', 2);

INSERT INTO classifiers_market_data_source VALUES
(1, 'Yahoo Fianance');