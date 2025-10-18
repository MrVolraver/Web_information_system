SELECT DATE(Entry_date), DATE(Exit_date), TIME(Entry_date), TIME(Exit_date), trollleybus_num, Stops_quanity, R_name, idlogin_password
FROM timesheet JOIN route USING (R_ID)
JOIN login_password USING (D_ID)
WHERE 1=1
$args
ORDER BY Entry_date