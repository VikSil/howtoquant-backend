#------------------------------------------------------------
# Seed Data
#------------------------------------------------------------

INSERT INTO marketdata_value_field VALUES
(1,'Open', 'Open',1),
(2,'High','High',1),
(3,'Low','Low',1),
(4,'Close','Close',1),
(5,'Adjusted Close','Adj Close',1),
(6,'Volume','Volume',1);

delimiter //
DROP PROCEDURE IF EXISTS populate_value_fields //
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
(2,2,2),
(3,3,3),
(4,4,4),
(5,5,5),
(6,6,6);


#------------------------------------------------------------
# Stored Procedures
#------------------------------------------------------------

delimiter //
DROP PROCEDURE IF EXISTS get_download_prices //
CREATE PROCEDURE get_download_prices(
	get_download_id int
)

BEGIN
	DECLARE price_ladder_content_id INT;
    
    SELECT id INTO price_ladder_content_id
	FROM django_content_type
	WHERE model = 'price_ladder';
    
	SELECT dd.value_date, dd.bid_price, dd.ask_price, t.code as ticker, vf.description as value_field, mds.source_name  as source FROM marketdata_download_data as dd
	LEFT JOIN staticdata_identifier as t ON dd.ticker_id = t.id
	LEFT JOIN marketdata_value_field as vf ON dd.value_field_id = vf.id
	LEFT JOIN classifiers_market_data_source as mds ON vf.market_data_source_id= mds.id
	WHERE download_id = get_download_id
	AND value_field_id IN (
		SELECT DISTINCT(value_field_id)
		FROM marketdata_value_field_to_spec
		WHERE value_spec_id IN (
			SELECT id FROM marketdata_value_spec
			WHERE ladder_id  = price_ladder_content_id
		)
	ORDER BY value_date, code, description
	);

END//
delimiter ;