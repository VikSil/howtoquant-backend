INSERT INTO staticdata_organization (id, short_name, long_name, org_type_id, description) VALUES
(1, 'Public Domain', 'The Public Domain Organization', 5,'The Default Internal Organization that owns all publically accessible data');

INSERT INTO staticdata_organization VALUES
(2, 'Tesla', 'Tesla Inc',7, 1,  'Tesla Inc'),
(3, 'Vodafone', 'Vodafone Group Plc',7, 1,  'Vodafone Group Plc'),
(4, 'VW', 'Volkswagen Group',7, 1,  'Volkswagen');

INSERT INTO staticdata_instrument VALUES
(1, 'Tesla Inc', 'Tesla', 5, 5, 5, 2,1),
(2, 'Vodafone Group Plc', 'Vodafone', 7, 7, 5, 3,1),
(3, 'Volkswagen Group', 'VW', 6, 6, 5, 4,1);

INSERT INTO staticdata_equity VALUES
(1, 4, 1, 5, 5),
(2, 4, 2, 6, 6),
(3, 4, 3, 5, 5);

INSERT INTO staticdata_identifier VALUES
(1, 'TSLA', 6, 1, 1),
(2, 'VOD', 6, 2, 1),
(3, 'VOW', 6, 3, 1);
