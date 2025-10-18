SELECT ticket_id, count, DATE(T_date), TIME(Entry_date), price, R_name, user_id
FROM basket JOIN timesheet ON basket.ticket_id=timesheet.T_ID
JOIN route USING (R_ID)
WHERE 1=1
$args