SELECT DATE(T_date), DATE(Exit_date), TIME(Entry_date), TIME(Exit_date), trollleybus_num, R_name, price, id_user
FROM route_history JOIN timesheet ON timesheet.T_ID=route_history.id_route
JOIN route USING (R_ID)
WHERE 1=1
$args
ORDER BY T_date