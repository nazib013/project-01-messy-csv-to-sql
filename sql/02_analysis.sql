-- Q1: How many transactions, how much revenue, and what is the average sale?
SELECT COUNT(*)                   AS transactions,
       SUM(total_spent)           AS revenue,
       ROUND(AVG(total_spent), 2) AS avg_transaction
FROM cafe_sales;

-- Q2: Which items bring in the most revenue?
SELECT COALESCE(item, 'Unknown') AS item,
       COUNT(*)                  AS transactions,
       SUM(total_spent)          AS revenue
FROM cafe_sales
GROUP BY item
ORDER BY revenue DESC;

-- Q3: How do customers pay?
SELECT COALESCE(payment_method, 'Unknown') AS payment_method,
       COUNT(*)                            AS transactions,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cafe_sales), 1) AS pct_of_transactions
FROM cafe_sales
GROUP BY payment_method
ORDER BY transactions DESC;

-- Q4: How much revenue per month?
SELECT strftime('%Y-%m', transaction_date) AS month,
       SUM(total_spent)                    AS revenue
FROM cafe_sales
WHERE transaction_date IS NOT NULL
GROUP BY month
ORDER BY month;