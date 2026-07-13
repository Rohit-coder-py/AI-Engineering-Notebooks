===========================================================
-- View data
-- =========================================================

SELECT * FROM customers;
SELECT * FROM categories;
SELECT * FROM products;
SELECT * FROM inventory;
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT * FROM payments;
SELECT * FROM shipping;
SELECT * FROM reviews;

-- ===========================================
-- Creating a view thats joins all the table together
-- ================================================
CREATE VIEW view_all_tables AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.phone,
    c.city AS customer_city,
    c.state AS customer_state,
    c.country AS customer_country,

    o.order_id,
    o.order_date,
    o.order_status,
    o.total_amount,

    oi.order_item_id,
    oi.quantity,
    oi.unit_price,

    p.product_id,
    p.product_name,
    p.brand,
    p.description AS product_description,
    p.price,
    p.status AS product_status,

    cat.category_id,
    cat.category_name,
    cat.description AS category_description,

    i.inventory_id,
    i.stock_quantity,
    i.reorder_level,
    i.last_updated,

    pay.payment_id,
    pay.payment_date,
    pay.payment_method,
    pay.payment_status,
    pay.amount AS payment_amount,

    s.shipping_id,
    s.address,
    s.city AS shipping_city,
    s.state AS shipping_state,
    s.country AS shipping_country,
    s.postal_code,
    s.shipping_date,
    s.delivery_date,
    s.shipping_status,

    r.review_id,
    r.rating,
    r.review_text,
    r.review_date

FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id

LEFT JOIN order_items oi
ON o.order_id = oi.order_id

LEFT JOIN products p
ON oi.product_id = p.product_id

LEFT JOIN categories cat
ON p.category_id = cat.category_id

LEFT JOIN inventory i
ON p.product_id = i.product_id

LEFT JOIN payments pay
ON o.order_id = pay.order_id

LEFT JOIN shipping s
ON o.order_id = s.order_id

LEFT JOIN reviews r
ON c.customer_id = r.customer_id
AND p.product_id = r.product_id;



Select * from view_all_tables

-- =========================================================
-- Queries on customers table
-- =========================================================

-- 1. Show all customers.
SELECT * FROM customers;

-- 2. Find a customer by email.
SELECT * FROM customers
WHERE email = 'aditya.kumar1@gmail.com';

-- 3. Count total customers.
SELECT COUNT(*) AS total_customers FROM customers;

-- 4. Find customers whose first name starts with 'A'.
SELECT * FROM customers
WHERE first_name LIKE 'A%';

-- 5. Count customers by city.
SELECT city, COUNT(*) AS total_customers
FROM customers
GROUP BY city
ORDER BY total_customers DESC;


-- =========================================================
-- Queries on products table
-- =========================================================

-- 6. Show all products with category name.
SELECT p.product_id, p.product_name, p.brand, p.price, c.category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id;

-- 7. Find products priced above 50000.
SELECT product_name, brand, price
FROM products
WHERE price > 50000
ORDER BY price DESC;

-- 8. Count products by category.
SELECT c.category_name, COUNT(p.product_id) AS total_products
FROM categories c
JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY total_products DESC;

-- 9. Find the most expensive product per category.
SELECT c.category_name, p.product_name, p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.price = (
    SELECT MAX(p2.price)
    FROM products p2
    WHERE p2.category_id = p.category_id
);


-- =========================================================
-- Queries on inventory table
-- =========================================================

-- 10. Products that are low on stock (at or below reorder level).
SELECT p.product_name, i.stock_quantity, i.reorder_level
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity ASC;

-- 11. Products that are completely out of stock.
SELECT p.product_name, i.stock_quantity
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.stock_quantity = 0;

-- 12. Total stock value held in inventory.
SELECT ROUND(SUM(p.price * i.stock_quantity), 2) AS total_inventory_value
FROM inventory i
JOIN products p ON i.product_id = p.product_id;


-- =========================================================
-- Queries on orders table
-- =========================================================

-- 13. Show all orders with customer name.
SELECT o.order_id, c.first_name, c.last_name, o.order_date, o.order_status, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;

-- 14. Count orders by status.
SELECT order_status, COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 15. Total revenue from delivered orders.
SELECT ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
WHERE order_status = 'Delivered';

-- 16. Monthly revenue trend.
SELECT TO_CHAR(order_date, 'YYYY-MM') AS order_month,
       ROUND(SUM(total_amount), 2) AS monthly_revenue,
       COUNT(*) AS total_orders
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY order_month;

-- 17. Cancellation rate.
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS cancellation_rate_percent
FROM orders;


-- =========================================================
-- Queries on order_items table (joins across orders / products)
-- =========================================================

-- 18. Full order detail: customer, products, quantity, and line total.
SELECT
    o.order_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    ROUND(oi.quantity * oi.unit_price, 2) AS line_total,
    o.order_status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id;

-- 19. Best-selling products by quantity sold.
SELECT p.product_name, SUM(oi.quantity) AS total_units_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_units_sold DESC
LIMIT 10;

-- 20. Top 10 customers by total amount spent.
SELECT c.customer_id, c.first_name, c.last_name,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 10;


-- =========================================================
-- Queries on payments table
-- =========================================================

-- 21. Revenue split by payment method.
SELECT payment_method, COUNT(*) AS total_payments, ROUND(SUM(amount), 2) AS total_amount
FROM payments
WHERE payment_status = 'Paid'
GROUP BY payment_method
ORDER BY total_amount DESC;

-- 22. Orders with pending or failed payments.
SELECT o.order_id, c.first_name, c.last_name, pay.payment_status, pay.amount
FROM payments pay
JOIN orders o ON pay.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE pay.payment_status IN ('Pending', 'Failed');


-- =========================================================
-- Queries on shipping table
-- =========================================================

-- 23. Orders currently in transit or preparing, with destination.
SELECT o.order_id, s.city, s.state, s.shipping_status, s.shipping_date, s.delivery_date
FROM shipping s
JOIN orders o ON s.order_id = o.order_id
WHERE s.shipping_status IN ('Preparing', 'In Transit')
ORDER BY s.shipping_date;

-- 24. Average delivery time (days) for delivered shipments.
SELECT ROUND(AVG(delivery_date - shipping_date), 1) AS avg_delivery_days
FROM shipping
WHERE shipping_status = 'Delivered';

-- 25. Orders shipped to each state.
SELECT state, COUNT(*) AS total_shipments
FROM shipping
GROUP BY state
ORDER BY total_shipments DESC;


-- =========================================================
-- Queries on reviews table
-- =========================================================

-- 26. Average rating per product.
SELECT p.product_name, ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(r.review_id) AS total_reviews
FROM reviews r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.product_name
ORDER BY avg_rating DESC, total_reviews DESC;

-- 27. Products with a rating below 3 (needs attention).
SELECT p.product_name, r.rating, r.review_text, c.first_name, c.last_name
FROM reviews r
JOIN products p ON r.product_id = p.product_id
JOIN customers c ON r.customer_id = c.customer_id
WHERE r.rating < 3;

-- 28. Most reviewed products.
SELECT p.product_name, COUNT(r.review_id) AS total_reviews
FROM reviews r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_reviews DESC
LIMIT 10;
