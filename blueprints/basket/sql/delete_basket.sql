DROP PROCEDURE IF EXISTS delete_basket;
delimiter //

CREATE PROCEDURE delete_basket (u_id INT)
BEGIN
	SET SQL_SAFE_UPDATES = 0;
    DELETE FROM f.basket
	WHERE user_id=u_id;
    SELECT '0';
END;

CALL delete_basket(2)