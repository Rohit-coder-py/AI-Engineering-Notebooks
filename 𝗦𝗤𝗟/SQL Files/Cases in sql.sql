----------------------------------------------------------------


-- Cases in SQL 

-- CASE is a conditional expression in SQL that works
-- like an if-else or switch statement. It lets you
-- return different values based on different
-- conditions - all within a single query.


-- WHY DO WE USE CASE?

-- . To create custom columns on-the-fly
-- · To categorize data based on certain logic
-- . To replace values conditionally
-- . To handle nulls or missing values gracefully


--basically if elif else (conditional statement) h ye sql ka 

-------------------------------------------------------------------------
-------------------------------------------------------------------------
                                 -- Syntax

Syntax of CASE in SQL


SELECT
column1,
CASE
WHEN condition1 THEN result1
WHEN condition2 THEN result2

...
ELSE default_result
END AS new_column_name
FROM table_name;

-------------------------------------------------------------------------
-------------------------------------------------------------------------


select * from flipkart_db;

Select product_name,price_max,
CASE when (price_max>1000) then 'Expensive'
     when (price_max between 500 and 100) then 'Moderate'
	 ELSE 'cheap'
End as price_tag from flipkart_db



-- adding this new column to flipkat_db

alter table flipkart_db
Add column price_tag varchar(20)

--now updating all values to new null table 

update flipkart_db
set price_tag =
case 
     when (price_max>1000) then 'Expensive'
     when (price_max between 500 and 1000) then 'Moderate'
	 ELSE 'cheap'
END;



-- Ok now lets do one important question inside is available
-- column you have boolean true and false show case a new
-- column to with in_stock and out of stock

Select product_name , is_available,
Case WHEN (is_available = True) then 'in_stock'
     When is_available = False then 'out of stock'
	 Else 'out_of_stock'
End as Stock_Status from flipkart_db;