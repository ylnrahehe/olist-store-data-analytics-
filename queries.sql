--4.b) basic checks and queries 
SELECT * 
FROM olist_customers_dataset 
LIMIT 10;

-- теперь показываем customer_name вместо customer_id
SELECT o.order_id, c.customer_name, o.order_status, o.order_purchase_timestamp
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
ORDER BY o.order_purchase_timestamp DESC
LIMIT 10;

SELECT order_status, COUNT(*) AS total_orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY total_orders DESC;

-- теперь customer_name вместо customer_id
SELECT o.order_id, c.customer_name, SUM(p.payment_value) AS total_payment
FROM olist_orders_dataset o
JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
GROUP BY o.order_id, c.customer_name
ORDER BY total_payment DESC
LIMIT 10;

--4.c) 10 analytical tasks
SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month, 
       AVG(p.payment_value) AS avg_order_value
FROM olist_orders_dataset o
JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
GROUP BY month
ORDER BY month; -- средняя сумма заказов в каждом месяце 

-- заменяем seller_id → seller_name
SELECT s.seller_name, SUM(oi.price) AS total_sales
FROM olist_order_items_dataset oi
JOIN olist_sellers_dataset s ON oi.seller_id = s.seller_id
GROUP BY s.seller_name
ORDER BY total_sales DESC
LIMIT 10; -- 10 продавцов с наибольшим количеством заказов 

SELECT customer_state, COUNT(DISTINCT customer_unique_id) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY total_customers DESC; -- сколько покупателей в каждом штате 

SELECT p.product_category_name, AVG(r.review_score) AS avg_score
FROM olist_order_items_dataset oi
JOIN olist_products_dataset p ON oi.product_id = p.product_id
JOIN olist_order_reviews_dataset r ON oi.order_id = r.order_id
GROUP BY p.product_category_name
ORDER BY avg_score DESC
LIMIT 10; -- средний рейтинг отзывов 

SELECT AVG(order_delivered_customer_date - order_purchase_timestamp) AS avg_delivery_days
FROM olist_orders_dataset
WHERE order_delivered_customer_date IS NOT NULL; -- сред время доставки

SELECT product_category_name, COUNT(*) AS total_products
FROM olist_products_dataset
GROUP BY product_category_name
ORDER BY total_products DESC
LIMIT 10; -- 10 видов продуктов и их количество

-- теперь customer_name вместо customer_id
SELECT c.customer_name, SUM(p.payment_value) AS total_spent
FROM olist_orders_dataset o
JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_spent DESC
LIMIT 10; --10 клиентов с наибольшеей суммой покупок

SELECT s.seller_state, AVG(oi.freight_value) AS avg_freight
FROM olist_order_items_dataset oi
JOIN olist_sellers_dataset s ON oi.seller_id = s.seller_id
GROUP BY s.seller_state
ORDER BY avg_freight DESC; --штаты и их средний прайз доставки 

SELECT order_status, COUNT(*) AS total_orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY total_orders DESC; --статусы заказов и их количество
