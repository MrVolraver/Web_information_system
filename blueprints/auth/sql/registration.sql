DROP PROCEDURE IF EXISTS registration;
delimiter //

CREATE PROCEDURE registration (login varchar(45), pass varchar(45), u_name varchar(45), u_surname varchar(45))
BEGIN
	DECLARE t_d INT;
    DECLARE pv INT DEFAULT 0;
	DECLARE DONE INTEGER DEFAULT 0;
	DECLARE t_money INTEGER;
    
    SELECT count(*) FROM login_password WHERE u_login = login into pv;
	IF pv = 0 THEN
		INSERT login_password (idlogin_password, u_login, u_password, u_role)
		VALUES (NULL, login, pass, "user");
        INSERT user_info (U_ID, name, surname)
        VALUES (LAST_INSERT_ID(), u_name, u_surname);
        SELECT '1';
	ELSE 
		SELECT '0';
	END IF;
END;

CALL registration ('111111', 'aaa', 'asdasda', 'asdasdasd');

SELECT * FROM login_password;