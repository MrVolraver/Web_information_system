DROP PROCEDURE IF EXISTS report;
delimiter //

CREATE PROCEDURE report (R_year INT)
BEGIN
	DECLARE t_d INT;
    DECLARE pv INT DEFAULT 0;
	DECLARE DONE INTEGER DEFAULT 0;
	DECLARE t_money INTEGER;
	DECLARE C1 CURSOR FOR SELECT YEAR(t_date), SUM(prod_price)
		FROM bought_history JOIN products
		USING (prod_id)
		WHERE YEAR(t_date) = R_year
		GROUP BY YEAR(t_date);
	DECLARE EXIT HANDLER FOR NOT FOUND SET DONE = 1;
    
    SELECT count(*) FROM report WHERE t_year = R_year into pv;
	IF pv = 0 THEN
		SELECT 'Всё окей';
		OPEN C1;
		WHILE DONE = 0 DO
			FETCH C1 INTO t_d, t_money;
			INSERT report (Rep_ID, t_year, Money)
			VALUES (NULL, R_year, t_money);
		END WHILE;
		CLOSE C1;
	ELSE 
		SELECT 'Уже существует отчёт с для такой даты';
	END IF;
END;

CALL report(2021);

SELECT * FROM report;