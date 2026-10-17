# SQL QUERIES 16 TO 20 

#Calculate average support resolution time by customer segment.
SELECT
    c.customer_segment,
    COUNT(*) AS resolved_tickets,
    ROUND(
        AVG(TIMESTAMPDIFF(
            HOUR, s.created_at, s.resolved_at
        )), 2
    ) AS avg_resolution_hours
FROM support_tickets s
JOIN crm_customers c
    ON s.customer_id = c.customer_id
WHERE s.resolved_at IS NOT NULL
GROUP BY c.customer_segment
ORDER BY avg_resolution_hours DESC;


 #Find customers with repeated support issues.
SELECT
    customer_id,
    COUNT(*) AS total_tickets,
    COUNT(DISTINCT issue_type) AS different_issue_types,
    MAX(created_at) AS last_ticket_date
FROM support_tickets
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY total_tickets DESC;

 #Rank customers within each segment using a window function.
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.customer_segment,
        COALESCE(SUM(p.payment_value), 0) AS lifetime_revenue
    FROM crm_customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN payments p ON o.order_id = p.order_id
    GROUP BY c.customer_id, c.customer_segment
)
SELECT
    customer_id,
    customer_segment,
    ROUND(lifetime_revenue, 2) AS lifetime_revenue,
    DENSE_RANK() OVER (
        PARTITION BY customer_segment
        ORDER BY lifetime_revenue DESC
    ) AS customer_rank
FROM customer_revenue
ORDER BY customer_segment, customer_rank;

 #Calculate each product/category's percentage contribution to total revenue.
WITH product_revenue AS (
    SELECT
        pr.product_id,
        pr.category,
        SUM(p.payment_value) AS total_revenue
    FROM orders o
    JOIN products pr ON o.product_id = pr.product_id
    JOIN payments p ON o.order_id = p.order_id
    GROUP BY pr.product_id, pr.category
)
SELECT
    product_id,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(
        100.0 * total_revenue
        / NULLIF(SUM(total_revenue) OVER (), 0),
        2
    ) AS revenue_contribution_pct
FROM product_revenue
ORDER BY total_revenue DESC;

 # Identify customers whose engagement is declining or whose activity indicates possible churn
WITH dataset_end AS (
    SELECT MAX(order_date) AS end_date
    FROM orders
),
order_activity AS (
    SELECT
        c.customer_id,
        SUM(CASE
            WHEN o.order_date >= DATE_SUB(
                d.end_date, INTERVAL 180 DAY
            )
            AND o.order_date < DATE_SUB(
                d.end_date, INTERVAL 90 DAY
            )
            THEN 1 ELSE 0
        END) AS previous_orders,
        SUM(CASE
            WHEN o.order_date >= DATE_SUB(
                d.end_date, INTERVAL 90 DAY
            )
            AND o.order_date <= d.end_date
            THEN 1 ELSE 0
        END) AS recent_orders
    FROM crm_customers c
    CROSS JOIN dataset_end d
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
)
SELECT
    customer_id,
    previous_orders,
    recent_orders,
    CASE
        WHEN recent_orders = 0 AND previous_orders > 0
            THEN 'Possible churn'
        WHEN recent_orders < previous_orders * 0.5
            THEN 'Declining engagement'
    END AS risk_status
FROM order_activity
WHERE previous_orders > 0
  AND (
      recent_orders = 0
      OR recent_orders < previous_orders * 0.5
  )
ORDER BY previous_orders DESC;
