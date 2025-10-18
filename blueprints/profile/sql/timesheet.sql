SELECT DATE(Entry_date), DATE(Exit_date), TIME(Entry_date), TIME(Exit_date), trollleybus_num, Stops_quanity, R_name
FROM timesheet JOIN route
USING (R_ID)