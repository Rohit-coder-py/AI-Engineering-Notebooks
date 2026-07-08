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
    orders.order_id,
    orders.customer_name,
    products.product_name,
    products.price
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

Select pr.product_name , pr.category,pr.price from products pr left join orders on products.product_id = orders.product_id
GROUP BY 




select * from products
select * from orders
