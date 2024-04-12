INSERT INTO marketdata_value_field VALUES
(1,'Open', 'Open', 1),
(2,'High','High',1),
(3,'Low','Low',1),
(4,'Close','Close',1),
(5,'Adjusted Close','Adj Close',1),
(6,'Volume','Volumne',1);

delimiter //
DROP PROCEDURE IF EXISTS populate_value_specs;
CREATE PROCEDURE populate_value_specs ()
BEGIN
	DECLARE price_ladder_content_id INT;
    DECLARE analytics_ladder_content_id INT;
    
    SELECT id INTO price_ladder_content_id
	FROM django_content_type
	WHERE model = 'price_ladder';

	SELECT id INTO analytics_ladder_content_id
	FROM django_content_type
	WHERE model = 'analytics_ladder';

	INSERT INTO marketdata_value_spec VALUES
	(1,'YF Prices','Prices from Yahoo Finance',@price_ladder_content_id,1,1),
	(2,'YF Analystics','Analytics from Yahoo Finance',@analytics_ladder_content_id,1,1);

END//
delimiter ;

CALL populate_value_specs();

INSERT INTO marketdata_value_field_to_spec VALUES
(1,1,1),
(2,2,1),
(3,3,1),
(4,4,1),
(5,5,1),
(6,6,2);
