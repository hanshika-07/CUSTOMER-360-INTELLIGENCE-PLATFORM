# SQL QUERIES 6 TO 10 

#Calculate monthly revenue and customer activity.
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    COUNT(DISTINCT o.customer_id) AS active_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;


# Calculate churn rate by customer segment.
WITH last_purchase AS (
    SELECT
        c.customer_id,
        c.customer_segment,
        MAX(o.order_date) AS last_order_date,
        (SELECT MAX(order_date) FROM orders) AS dataset_end
    FROM crm_customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_segment
),
churn_status AS (
    SELECT *,
        CASE
            WHEN last_order_date IS NULL
              OR last_order_date < DATE_SUB(dataset_end, INTERVAL 90 DAY)
            THEN 1 ELSE 0
        END AS is_churned
    FROM last_purchase
)
SELECT
    customer_segment,
    COUNT(*) AS total_customers,
    SUM(is_churned) AS churned_customers,
    ROUND(100.0 * SUM(is_churned) / COUNT(*), 2) AS churn_rate_pct
FROM churn_status
GROUP BY customer_segment
ORDER BY churn_rate_pct DESC;


# Calculate retention rate by customer segment.
WITH dataset_end AS (
    SELECT MAX(order_date) AS end_date FROM orders
),
activity AS (
    SELECT
        c.customer_id,
        c.customer_segment,
        MAX(CASE
            WHEN o.order_date >= DATE_SUB(d.end_date, INTERVAL 180 DAY)
             AND o.order_date < DATE_SUB(d.end_date, INTERVAL 90 DAY)
            THEN 1 ELSE 0
        END) AS previous_active,
        MAX(CASE
            WHEN o.order_date >= DATE_SUB(d.end_date, INTERVAL 90 DAY)
             AND o.order_date <= d.end_date
            THEN 1 ELSE 0
        END) AS current_active
    FROM crm_customers c
    CROSS JOIN dataset_end d
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_segment
)
SELECT
    customer_segment,
    SUM(previous_active) AS previous_customers,
    SUM(previous_active * current_active) AS retained_customers,
    ROUND(
        100.0 * SUM(previous_active * current_active)
        / NULLIF(SUM(previous_active), 0), 2
    ) AS retention_rate_pct
FROM activity
GROUP BY customer_segment
ORDER BY retention_rate_pct DESC;


# Find customers with high purchase frequency or high transaction value.
SELECT
    o.customer_id,
    COUNT(DISTINCT o.order_id) AS purchase_frequency,
    ROUND(SUM(p.payment_value), 2) AS total_transaction_value
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY o.customer_id
HAVING COUNT(DISTINCT o.order_id) >= 5
    OR SUM(p.payment_value) >= 10000
ORDER BY total_transaction_value DESC;
    
    
# Find customers whose lifetime value exceeds a selected threshold.
SELECT
    o.customer_id,
    COUNT(DISTINCT o.order_id) AS lifetime_orders,
    ROUND(SUM(p.payment_value), 2) AS lifetime_value
FROM orders o
JOIN payments p ON o.order_id = p.order_id
GROUP BY o.customer_id
HAVING SUM(p.payment_value) > 5000
ORDER BY lifetime_value DESC;
