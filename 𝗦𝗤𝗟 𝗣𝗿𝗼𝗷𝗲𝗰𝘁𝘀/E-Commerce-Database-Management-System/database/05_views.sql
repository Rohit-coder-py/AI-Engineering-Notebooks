-- =========================================================
-- 1. order_summary
-- =========================================================
CREATE OR REPLACE VIEW order_summary AS
SELECT
    o.order_id,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    o.order_date,
    o.order_status,
    o.total_amount,
    pay.payment_method,
    pay.payment_status,
    s.shipping_status,
    s.city AS shipping_city,
    s.state AS shipping_state
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN payments pay ON o.order_id = pay.order_id
LEFT JOIN shipping s ON o.order_id = s.order_id;

-- Select * from order_summary;


-- =========================================================
-- 2. product_catalog
-- Product details joined with category and current stock level.
-- =========================================================
CREATE OR REPLACE VIEW product_catalog AS
SELECT
    p.product_id,
    p.product_name,
    p.brand,
    c.category_name,
    p.price,
    p.status,
    i.stock_quantity,
    i.reorder_level,
    CASE
        WHEN i.stock_quantity = 0 THEN 'Out of Stock'
        WHEN i.stock_quantity <= i.reorder_level THEN 'Low Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN inventory i ON p.product_id = i.product_id;

-- Select * from product_catalog;


-- =========================================================
-- 3. inventory_alert
-- Products that need restocking (low stock or out of stock).
-- =========================================================
CREATE OR REPLACE VIEW inventory_alert AS
SELECT
    p.product_id,
    p.product_name,
    p.brand,
    i.stock_quantity,
    i.reorder_level
FROM products p
JOIN inventory i ON p.product_id = i.product_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity ASC;

-- Select * from inventory_alert;


-- =========================================================
-- 4. customer_spending
-- Total orders and lifetime spend per customer.
-- =========================================================
CREATE OR REPLACE VIEW customer_spending AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    c.state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) AS lifetime_spend
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city, c.state;

-- Select * from customer_spending order by lifetime_spend desc;


-- =========================================================
-- 5. monthly_revenue
-- Revenue and order volume grouped by calendar month.
-- =========================================================
CREATE OR REPLACE VIEW monthly_revenue AS
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS order_month,
    COUNT(*) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY order_month;

-- Select * from monthly_revenue;


-- =========================================================
-- 6. product_ratings
-- Average rating and review count per product.
-- =========================================================
CREATE OR REPLACE VIEW product_ratings AS
SELECT
    p.product_id,
    p.product_name,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.review_id) AS total_reviews
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.product_name;

Select * from product_ratings order by avg_rating desc nulls last;


-- =========================================================
-- 7. all_joined
-- A single wide view joining every table together, similar in
-- spirit to a full denormalized export of the whole system.
-- =========================================================
CREATE OR REPLACE VIEW all_joined AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    c.state,

    o.order_id,
    o.order_date,
    o.order_status,
    o.total_amount,

    p.product_name,
    cat.category_name,
    oi.quantity,
    oi.unit_price,

    pay.payment_method,
    pay.payment_status,

    s.shipping_status,
    s.shipping_date,
    s.delivery_date

FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
LEFT JOIN payments pay ON o.order_id = pay.order_id
LEFT JOIN shipping s ON o.order_id = s.order_id;

Select * from all_joined order by order_id desc;
