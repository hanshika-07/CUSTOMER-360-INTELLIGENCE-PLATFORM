# SQL QUERIES 1 TO 5 

 #Calculate total customers by state/city.
SELECT
    state,
    city,
    COUNT(DISTINCT customer_id) AS total_customers
FROM crm_customers
GROUP BY state, city
ORDER BY total_customers DESC;


 #Calculate average customer value by customer segment.
 WITH customer_value AS (
    SELECT
        o.customer_id,
        SUM(p.payment_value) AS lifetime_value
    FROM orders o
    JOIN payments p ON o.order_id = p.order_id
    GROUP BY o.customer_id
)
SELECT
    c.customer_segment,
    ROUND(AVG(COALESCE(cv.lifetime_value, 0)), 2)
        AS avg_customer_value
FROM crm_customers c
LEFT JOIN customer_value cv
    ON c.customer_id = cv.customer_id
GROUP BY c.customer_segment
ORDER BY avg_customer_value DESC;


 #Find the top 10 products by total revenue.
SELECT
    p.product_id,
    p.product_name,
    ROUND(SUM(pay.payment_value), 2) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN payments pay ON o.order_id = pay.order_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC
LIMIT 10;


 #Find the top 10 customers by total transaction value.
SELECT
    o.customer_id,
    ROUND(SUM(p.payment_value), 2) AS total_transaction_value
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY o.customer_id
ORDER BY total_transaction_value DESC
LIMIT 10;
 
 
 #Calculate total transactions and revenue by product category
 SELECT
    pr.category,
    COUNT(DISTINCT o.order_id) AS total_transactions,
    ROUND(SUM(pay.payment_value), 2) AS total_revenue
FROM orders o
JOIN products pr ON o.product_id = pr.product_id
JOIN payments pay ON o.order_id = pay.order_id
GROUP BY pr.category
ORDER BY total_revenue DESC;
