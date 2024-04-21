#------------------------------------------------------------
# Seed Data
#------------------------------------------------------------

INSERT INTO marketdata_value_field VALUES
(1,'Open', 'Open',5),
(2,'High','High',5),
(3,'Low','Low',5),
(4,'Close','Close',5),
(5,'Adjusted Close','Adj Close',5),
(6,'Volume','Volume',5);

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
		))
	ORDER BY value_date, code, description
	;

END//
delimiter ;

#------------------------------------------------------------

delimiter //
DROP PROCEDURE IF EXISTS save_download_prices //
CREATE PROCEDURE save_download_prices(
	get_download_id int,
    -- 0: save missing, 1: override all
    override int
)

BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE price_ladder_content_id, c_inst_id, c_ticker_id, c_value_field_id, existing_row_count INT;
    DECLARE c_value_date DATE;
    DECLARE c_bid_price, c_ask_price DOUBLE;

    DECLARE download_cursor CURSOR FOR 
		SELECT value_date, bid_price, ask_price, instrument_id, ticker_id, value_field_id 
        FROM marketdata_download_data 
        WHERE download_id = get_download_id 
		AND value_field_id IN (
			SELECT DISTINCT(value_field_id)
			FROM marketdata_value_field_to_spec
			WHERE value_spec_id IN (
				SELECT id FROM marketdata_value_spec
				WHERE ladder_id  = 22
			));
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
	SELECT id INTO price_ladder_content_id
	FROM django_content_type
	WHERE model = 'price_ladder';

	SELECT requested_start_date INTO @req_start_dt
    FROM marketdata_download 
    WHERE id = get_download_id;
    
	SELECT requested_end_date INTO @req_end_dt
    FROM marketdata_download
    WHERE id = get_download_id;   
	
    SET @timing = DATE_FORMAT(now(), '%Y%m%d_%H%i%s');
    SET @temp_table_name  = CONCAT('marketdata_price_ladder_temp_',get_download_id,'_',@timing);

	-- CREATE TEMP TABLE FROM PRICE LADDER	
	SET @create_query = CONCAT('CREATE TABLE ',@temp_table_name,'
    (temp_id bigint PRIMARY KEY AUTO_INCREMENT) 
    select * from marketdata_price_ladder
	WHERE value_date>= \'',@req_start_dt,
	'\' AND value_date<= \'',@req_end_dt,
	'\' AND ticker_id IN (SELECT DISTINCT(ticker_id) FROM marketdata_download_tickers WHERE download_id = ', get_download_id,' )
	AND value_field_id IN (SELECT DISTINCT(value_field_id) FROM marketdata_download_data WHERE download_id = ', get_download_id, ' )'
    );
    
	PREPARE stmt from @create_query;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;

	SET @some_variable:=-1;
	SET @count_query = CONCAT('SELECT COUNT(*) INTO @some_variable FROM ',@temp_table_name);
	PREPARE stmt from @count_query;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	
    -- IF THE TEMP TABLE IS EMPTY, SAVE ALL PRICES FROM DOWNLOAD DATA
    IF @some_variable = 0 THEN
		OPEN download_cursor;        
        save_loop: LOOP
			FETCH download_cursor INTO c_value_date, c_bid_price, c_ask_price, c_inst_id, c_ticker_id, c_value_field_id;
			IF done = 1 THEN
                LEAVE save_loop;
            END IF;
            INSERT INTO marketdata_price_ladder (value_date, bid_price, ask_price, download_id, instrument_id, owner_org_id, ticker_id, value_field_id) 
			VALUES (c_value_date, c_bid_price, c_ask_price, get_download_id, c_inst_id, 1, c_ticker_id, c_value_field_id);
		END LOOP save_loop;
        CLOSE download_cursor;
        
    -- IF PREVIOUS PRICE RECORDS EXIST ITERATE OVER DOWNLOAD ROWS
    ELSE
		OPEN download_cursor;
        iterrate_loop: LOOP
			FETCH download_cursor INTO c_value_date, c_bid_price, c_ask_price, c_inst_id, c_ticker_id, c_value_field_id;
			IF done = 1 THEN
                LEAVE iterrate_loop;
            END IF;
            -- LOOK FOR PRICE TABLE RECORD FOR SAME DATE, TICKER, VALUE_FIELD AS IN DOWNLOAD RECORD
            SET @old_record_id:= -1;
            SET @find_record = CONCAT('SELECT id INTO @old_record_id FROM ', @temp_table_name,' WHERE value_date = \'',c_value_date,'\' AND ticker_id = ', c_ticker_id, ' AND value_field_id = ', c_value_field_id, ' AND owner_org_id = 1');
            PREPARE stmt from @find_record;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
            
            IF @old_record_id <0 THEN -- NO PREVIOUS RECORD FOUND
				INSERT INTO marketdata_price_ladder (value_date, bid_price, ask_price, download_id, instrument_id, owner_org_id, ticker_id, value_field_id) 
				VALUES (c_value_date, c_bid_price, c_ask_price, get_download_id, c_inst_id, 1, c_ticker_id, c_value_field_id);            
            ELSEIF override = 1 THEN  -- PREVIOUS RECORD FOUND AND OVERRIDE SET
				UPDATE marketdata_price_ladder
                SET bid_price = c_bid_price, ask_price= c_ask_price, download_id = get_download_id, instrument_id = c_inst_id 
                WHERE id = @old_record_id;
            ELSE 
				BEGIN END;
            END IF;
        END LOOP iterrate_loop;
        CLOSE download_cursor;    
    END IF;
    
	SET @delete_query = CONCAT('DROP TABLE ',@temp_table_name);
	PREPARE stmt from @delete_query;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;

END//
delimiter ;