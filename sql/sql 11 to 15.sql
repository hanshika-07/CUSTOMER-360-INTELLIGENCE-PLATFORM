# SQL QUERIES 11 TO 15 


# Find cities/segments with above-average customer value.
WITH customer_value AS (
    SELECT
        c.customer_id,
        c.city,
        c.state,
        c.customer_segment,
        COALESCE(SUM(p.payment_value), 0) AS lifetime_value
    FROM crm_customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN payments p ON o.order_id = p.order_id
    GROUP BY
        c.customer_id, c.city, c.state, c.customer_segment
)
SELECT
    city,
    state,
    customer_segment,
    COUNT(*) AS total_customers,
    ROUND(AVG(lifetime_value), 2) AS avg_customer_value
FROM customer_value
GROUP BY city, state, customer_segment
HAVING AVG(lifetime_value) > (
    SELECT AVG(lifetime_value) FROM customer_value
)
ORDER BY avg_customer_value DESC;


 #Calculate average transaction amount by channel.
 WITH transaction_values AS (
    SELECT
        o.order_id,
        o.channel,
        SUM(p.payment_value) AS transaction_amount
    FROM orders o
    JOIN payments p ON o.order_id = p.order_id
    GROUP BY o.order_id, o.channel
)
SELECT
    channel,
    COUNT(*) AS total_transactions,
    ROUND(AVG(transaction_amount), 2) AS avg_transaction_amount,
    ROUND(SUM(transaction_amount), 2) AS total_transaction_value
FROM transaction_values
GROUP BY channel
ORDER BY avg_transaction_amount DESC;


 #Find the top 10 customers by engagement activity.
WITH engagement AS (
    SELECT customer_id, COUNT(*) AS activity_count
    FROM marketing_interactions
    GROUP BY customer_id

    UNION ALL

    SELECT customer_id, COUNT(*) AS activity_count
    FROM product_usage
    GROUP BY customer_id
)
SELECT
    customer_id,
    SUM(activity_count) AS total_engagement_activities
FROM engagement
GROUP BY customer_id
ORDER BY total_engagement_activities DESC
LIMIT 10;


 #Calculate monthly active customers.
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(DISTINCT customer_id) AS monthly_active_customers
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;


 #Find customers with no recent transactions or interactions
 WITH last_activity AS (
    SELECT
        c.customer_id,
        MAX(o.order_date) AS last_order_date,
        (SELECT MAX(order_date) FROM orders) AS dataset_end
    FROM crm_customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
)
SELECT
    customer_id,
    last_order_date,
    CASE
        WHEN last_order_date IS NULL THEN 'Never purchased'
        ELSE 'No purchase in last 90 days'
    END AS activity_status
FROM last_activity
WHERE last_order_date IS NULL
   OR last_order_date < DATE_SUB(dataset_end, INTERVAL 90 DAY)
ORDER BY last_order_date;