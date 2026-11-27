-- Q1: Revenue and transaction count by location
SELECT COALESCE(location, 'Unknown') AS location,
       COUNT(transaction_id)         AS transaction_count,
       SUM(total_spent)              AS revenue
FROM cafe_sales
GROUP BY location
ORDER BY revenue DESC;

-- Q2: Average quantity per transaction for each item
SELECT COALESCE(item, 'Unknown')  AS item,
       ROUND(AVG(quantity), 2)    AS avg_quantity
FROM cafe_sales
GROUP BY item
ORDER BY avg_quantity DESC;

-- Q3: Busiest day of the week (0 = Sunday, 6 = Saturday)
SELECT strftime('%w', transaction_date) AS day_number,
       COUNT(*)                         AS transactions
FROM cafe_sales
WHERE transaction_date IS NOT NULL
GROUP BY day_number
ORDER BY transactions DESC;

-- Q4: Month-over-month revenue change
WITH monthly AS (
    SELECT strftime('%Y-%m', transaction_date) AS month,
           SUM(total_spent)                    AS revenue
    FROM cafe_sales
    WHERE transaction_date IS NOT NULL
    GROUP BY month
)
SELECT month,
       revenue,
       LAG(revenue) OVER (ORDER BY month)           AS prev_revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS revenue_change
FROM monthly
ORDER BY month;