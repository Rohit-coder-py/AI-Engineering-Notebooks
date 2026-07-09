CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category TEXT,
    price NUMERIC(10,2),
    stock_quantity INT,
    is_available BOOLEAN,
    added_on DATE
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    product_id INT,
    quantity INT,
    order_date DATE,
    customer_name VARCHAR(50),
    payment_method VARCHAR(50),

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);

select * from products
select * from orders


===================================================================
===================================================================


-- Q1. Show each order along with the product name and price 

SELECT
    products.product_name,
    products.price orders.order_id,
    orders.customer_name,
   
FROM products
INNER JOIN orders
ON products.product_id = orders.product_id;


-- Q2. Show all products even if they were never ordered.

SELECT
    products.product_name
FROM products
LEFT JOIN orders
ON products.product_id = orders.product_id;


-- Q3.Show orders for only 'Electronics' category.

Select * from products left join orders on products.product_id = orders.product_id
where products.category = 'Electronics'


-- Q4.List all orders sorted by product price (high to low)

Select pr.product_name , pr.category,pr.price from products pr left join orders on pr.product_id = orders.product_id
ORDER BY pr.price DESC;


-- Q5.Show number of orders placed for each product.

SELECT p.product_name,COUNT(o.order_id) AS total_orders 
FROM products p INNER JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_name;




-- Q6.Show total revenue earned per product.

SELECT
    p.product_name,
    SUM(p.price * o.quantity) AS total_revenue
FROM products p
INNER JOIN orders o
ON p.product_id = o.product_id
GROUP BY p.product_name;





-- Q7.Show products where total order revenue > ₹2000.


SELECT
    p.product_name,
    SUM(p.price * o.quantity) AS total_revenue
FROM products p
INNER JOIN orders o
ON p.product_id = o.product_id
GROUP BY p.product_name
Having SUM(p.price * o.quantity)>2000;



-- Q8.Show unique customers who ordered 'Fitness' products.

SELECT DISTINCT
    o.customer_name
FROM products p
INNER JOIN orders o
ON p.product_id = o.product_id
WHERE p.category = 'Fitness';
s
