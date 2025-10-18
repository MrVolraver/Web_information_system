DROP PROCEDURE IF EXISTS create_order_details;
delimiter //

CREATE PROCEDURE create_order_details (orderid INT, product INT, count_it INT)
BEGIN
	INSERT order_details (idorder_details, id_order, product_id, count)
	VALUES (NULL, orderid, product, count_it);
    SELECT '0';
END;

CALL create_order_details(1, 1, 2, 100);

SELECT * FROM order_details;