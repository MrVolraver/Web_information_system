SELECT DATE(T_date), DATE(Exit_date), TIME(Entry_date), TIME(Exit_date), trollleybus_num, Stops_quanity, R_name, T_ID, price, remain_count_ticket
FROM timesheet JOIN route
USING (R_ID)
WHERE 1=1
$args