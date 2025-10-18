DROP PROCEDURE IF EXISTS create_order;
delimiter //

CREATE PROCEDURE create_order (id INT, totalsum INT)
BEGIN
	INSERT orders (idorders, data_order, user_id1, status, total_sum)
	VALUES (NULL, NOW(), id, 0, totalsum);
    SELECT LAST_INSERT_ID();
END;

CALL create_order(2, 2739);

SELECT * FROM orders;