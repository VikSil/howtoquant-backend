INSERT INTO classifiers_identifier_type VALUES
(1, 'Unknown'),
(2, 'Unspecified'),
(3, 'None'),
(4, 'Other'),
(5, 'ISIN'),
(6, 'BBG Ticker'),
(7, 'Sedol'),
(8, 'RIC'),
(9, 'Internal Ticker'),
(10, 'BBG Exchange Code'),
(11, 'CIK'),
(12, 'FIGI');

INSERT INTO classifiers_instrument_class VALUES
(1, 'Unknown','Unknown'),
(2, 'Unspecified','Unspecified'),
(3, 'None','None'),
(4, 'Other','Other'),
(5, 'Equity', 'Simple Stock');

INSERT INTO classifiers_currency VALUES
(1, 'Unknown','Unknown',0,'XYZ'),
(2, 'Unspecified','Unspecified',0,'XZY'),
(3, 'None','None',0,'YXZ'),
(4, 'Other','Other',0,'YZX'),
(5, 'United States Dollar', 'Cent', 100, 'USD'),
(6, 'Euro', 'Cent', 100, 'EUR'),
(7, 'Pound sterling', 'Pence', 100, 'GBP'),
(8, 'Swiss frank', 'Rappen/Centime', 1000, 'CHF'),
(9, 'Japanese yen', '', 0, 'JPY');

INSERT INTO classifiers_country VALUES
(1, 'Unknown','Unknown','XX','XYZ',1),
(2, 'Unspecified','Unspecified','YY','XZY',2),
(3, 'None','None','XY','YXZ',3),
(4, 'Other','Other','ZZ','YZX',4),
(5, 'The United States of America', 'USA', 'US', 'USA', 5),
(6, 'The Federal Republic of Germany', 'Germany', 'DE', 'DEU' , 6),
(7, 'The United Kingdom of Great Britain and Northern Ireland', 'UK', 'GB', 'GBR' , 7),
(8, 'The Swiss Confederation', 'Switzerland', 'CH', 'CHE' , 8),
(9, 'Japan', 'Japan', 'JP', 'JPN', 9);

INSERT INTO classifiers_organization_type VALUES
(1, 'Unknown'),
(2, 'Unspecified'),
(3, 'None'),
(4, 'Other'),
(5, 'Internal'),
(6, 'Headquarters'),
(7, 'Issuer');

INSERT INTO classifiers_industry_sector VALUES
(1, 'Unknown'),
(2, 'Unspecified'),
(3, 'None'),
(4, 'Other'),
(5, 'Automotive'),
(6, 'Telecommunications');

INSERT INTO classifiers_industry_subsector VALUES
(1, 'Unknown',1),
(2, 'Unspecified',2),
(3, 'None',3),
(4, 'Other',4),
(5, 'Automotive', 5),
(6, 'Telecommunications', 6);

INSERT INTO classifiers_market_data_source VALUES
(1, 'Unknown',''),
(2, 'Unspecified',''),
(3, 'None',''),
(4, 'Other',''),
(5, 'Yahoo Finance Prices','get_yf_price_data');