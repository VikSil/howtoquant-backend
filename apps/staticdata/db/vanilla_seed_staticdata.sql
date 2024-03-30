INSERT INTO staticdata_organization (short_name, long_name, org_type_id_id, description) VALUES
('Public Domain', 'The Public Domain Organization', 1,'The Default Internal Organization that owns all publically accessible data');

INSERT INTO staticdata_organization VALUES
(2, 'Tesla', 'Tesla Inc',3, 1,  'Tesla Inc'),
(3, 'Vodafone', 'Vodafone Group Plc',3, 1,  'Vodafone Group Plc'),
(4, 'VW', 'Volkswagen Group',3, 1,  'Volkswagen');

INSERT INTO staticdata_instrument VALUES
(1, 'Tesla Inc', 'Tesla', 1, 1, 1, 2,1),
(2, 'Vodafone Group Plc', 'Vodafone', 3, 3, 1, 3,1),
(3, 'Volkswagen Group', 'VW', 2, 2, 1, 4,1);

INSERT INTO staticdata_equity VALUES
(1, 4, 1, 1, 1),
(2, 4, 2, 2, 2),
(3, 4, 3, 1, 1);

INSERT INTO staticdata_identifier VALUES
(1, 'TSLA', 2, 1, 1),
(2, 'VOD', 2, 2, 1),
(3, 'VOW', 2, 3, 1);
