# сколько уникальных пользователей делали заказ в месяц

SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(DISTINCT customer_id) AS mau
FROM ecommerce.orders
GROUP BY month
ORDER BY month;

# сколько заказов у каждого клиента

SELECT customer_id, COUNT(order_id) AS order_count
FROM ecommerce.orders
GROUP BY customer_id
ORDER BY order_count DESC
LIMIT 10;

# 10 самых продаваемых продуктов

SELECT
    p.product_id,
    p.product_category_name,
    SUM(oi.price) AS total_sales
FROM ecommerce.order_items oi
JOIN ecommerce.products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_category_name
ORDER BY total_sales DESC
LIMIT 10;

# Средний чек

SELECT AVG(order_sum) AS avg_order_value
FROM (
    SELECT order_id,
           SUM(payment_value) AS order_sum
    FROM ecommerce.payments
    GROUP BY order_id
) t;

Средняя оценка товара

SELECT
    r.review_score,
    COUNT(*) AS review_count
FROM ecommerce.reviews r
GROUP BY r.review_score
ORDER BY r.review_score DESC;