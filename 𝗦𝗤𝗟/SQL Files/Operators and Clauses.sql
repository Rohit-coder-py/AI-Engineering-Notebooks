-- Clauses with operators and aggregationm function 

----Operators : 

-- Comparison
-- Logical
-- Range
-- Membership
-- Pattern Matching
-- Null Checking
-- Existence (later)


-- 1. Comparision : =, !=, <>, >, <, >=, <=


Select * from flipkart_db;


Select * from flipkart_db where Category = 'Electronics';


Select * from flipkart_db where Category != 'Electronics';

Select * from flipkart_db where Category <> 'Electronics';            -- <> = not equal to 

Select * from flipkart_db where price_max > 999;

Select COUNT(*) from flipkart_db where price_max > 999;

-- Logical (AND, OR, NOT)

Select * from flipkart_db where price_max > 999 and category = 'Electronics';

SELECT * FROM flipkart_db WHERE category = 'Electronics' OR category = 'Furniture';

SELECT * FROM flipkart_db WHERE NOT category = 'Electronics';
--Range (BETWEEN)

Select * from flipkart_db where price_max Between 1000 and 4000;


--Membership (IN, NOT IN)

Select * from flipkart_db where category in ('Electronics','Furniture','Wearables')


Select * from flipkart_db where category NOT IN ('Electronics','Furniture','Wearables')


--  Pattern Matching (LIKE, ILIKE,NOT LIKE)

Select * from flipkart_db where product_name like 'P%';            -- P in start 

Select * from flipkart_db where product_name like '%C%';           -- C in middle 

-- % means start 
-- % means end

Select * from flipkart_db where product_name like '_a%';           --second character should be 'a'



-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------


-- Now Aggregate Functions 

-- COUNT()
-- SUM()
-- AVG() 
-- MIN()
-- MAX()

SELECT AGGREGATE_FUNCTION(column_name) FROM table_name WHERE condition;

--COUNT()

Select COUNT(product_id) from flipkart_db 

Select COUNT(product_id) from flipkart_db where price_max>1000;


--SUM()

-- Only for numeric columns 

Select SUM(price_max) from flipkart_db;

Select SUM(price_max) from flipkart_db where category = 'Electronics';

--AVG()

Select AVG(price_max) from flipkart_db;

Select round(AVG(price_max),2) from flipkart_db;



--MIN()

Select Min(price_max) from flipkart_db;

Select * from flipkart_db where price_max = 99;


--MAX()

Select MAX(price_max) from flipkart_db;


Select MAX(price_max) from flipkart_db where category = 'Electronics' or category = 'Furniture';


--- Test Time

-- Q1. Display the name and price of the cheapest product in the
-- entire table


Select * from flipkart_db;

SELECT product_name, price_max FROM flipkart_db ORDER BY price_max ASC LIMIT 1;


-- Q2.Find the average price of products that belong to the 'Home &
-- Kitchen' or 'Fitness' category


Select AVG(price_max) from flipkart_db where category in ('Home & Kitchen','Fitness');


-- Q3. Show product names and stock quantity where the product is
-- available, stock is more than 50, and price is not equal to ₹299.


Select product_name,stock_quantity from Flipkart_db where stock_quantity >=50 and  price_max !=299;

-- Q4. Find the most expensive product in each category (name and price).

SELECT DISTINCT UPPER(category) FROM flipkart_db ORDER BY UPPER(category) DESC;


-- Q5. Show all unique categories in uppercase, sorted in descer
-- order

SELECT DISTINCT UPPER(category) FROM flipkart_db ORDER BY UPPER(category) DESC;

