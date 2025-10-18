SELECT user_id1, id_order, count, T_date, price, R_name
FROM orders JOIN order_details ON orders.idorders=order_details.id_order 
JOIN timesheet ON timesheet.T_ID=order_details.product_id
JOIN route USING (R_ID)
WHERE 1=1
$args
ORDER BY T_date