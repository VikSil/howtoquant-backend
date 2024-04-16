INSERT INTO marketdata_value_field VALUES
(1,'Open', 'Open',1),
(2,'High','High',1),
(3,'Low','Low',1),
(4,'Close','Close',1),
(5,'Adjusted Close','Adj Close',1),
(6,'Volume','Volume',1);

delimiter //
DROP PROCEDURE IF EXISTS populate_value_fields;
CREATE PROCEDURE populate_value_fields ()
BEGIN
	DECLARE price_ladder_content_id INT;
    DECLARE analytics_ladder_content_id INT;
    
    SELECT id INTO price_ladder_content_id
	FROM django_content_type
	WHERE model = 'price_ladder';

	SELECT id INTO analytics_ladder_content_id
	FROM django_content_type
	WHERE model = 'analytics_ladder';

	INSERT INTO marketdata_value_spec (id,name,description, ladder_id, owner_org_id) VALUES
	(1,'Open', 'Daily Open Price',price_ladder_content_id,1),
	(2,'High','Daily High Price',price_ladder_content_id,1),
	(3,'Low','Daily Low Price',price_ladder_content_id,1),
	(4,'Close','Market Close Price EOD',price_ladder_content_id,1),
	(5,'Adjusted Close','Adj Close Price EOD',price_ladder_content_id,1),
	(6,'Volume','Daily Volume',analytics_ladder_content_id,1);

END//
delimiter ;

CALL populate_value_fields();

INSERT INTO marketdata_value_field_to_spec VALUES
(1,1,1),
(2,2,1),
(3,3,1),
(4,4,1),
(5,5,1),
(6,6,1);
