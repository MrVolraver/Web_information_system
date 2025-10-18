SELECT data_order, user_id1, status, total_sum, idorders
FROM orders JOIN order_details ON orders.idorders=order_details.id_order
JOIN timesheet ON timesheet.T_ID=order_details.product_id
JOIN route USING (R_ID)
WHERE 1=1
$args
GROUP BY idorders
ORDER BY data_order DESC
