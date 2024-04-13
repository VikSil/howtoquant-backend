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

	INSERT INTO marketdata_value_field (id,description, field_name, ladder_id, owner_org_id) VALUES
	(1,'Open', 'Open',price_ladder_content_id,1),
	(2,'High','High',price_ladder_content_id,1),
	(3,'Low','Low',price_ladder_content_id,1),
	(4,'Close','Close',price_ladder_content_id,1),
	(5,'Adjusted Close','Adj Close',price_ladder_content_id,1),
	(6,'Volume','Volume',analytics_ladder_content_id,1);

END//
delimiter ;

CALL populate_value_fields();

INSERT INTO marketdata_value_spec VALUES
(1,'YF Download','Daily prices and Volume from Yahoo Finance',1,1);

INSERT INTO marketdata_value_field_to_spec VALUES
(1,1,1),
(2,2,1),
(3,3,1),
(4,4,1),
(5,5,1),
(6,6,1);
