A view is a virtual table based on a SQL query.
It does not store actual data, but shows results when
accessed - just like a saved query


* Simplify Complex Queries
  Save a long query and access it like a table.

* Reuse Logic
  No need to rewrite JOINs or filters again and again.

* Security
  Expose only selected columns instead of giving full access to the table.

* Abstraction
  Hide table complexity for front-end/dashboard users.

* Maintainability
  If the logic changes, update the view once and the changes reflect everywhere.


============================================
============================================

Syntax : 
CREATE VIEW view_name AS
SELECT column1, column2
FROM table_name
WHERE condition;




select * from flipkart_db


CREATE VIEW expensive_products AS
SELECT product_name, price_max
FROM flipkart_db
WHERE price_max > 1000;

SELECT * FROM expensive_products;



-- Create a views for low stock items 

select * from flipkart_db



Create view low_stock as 
Select product_name , stock_quantity 
From flipkart_db
where stock_quantity <20;


Select * from low_stock



======================================================================================
                               Views COMPLETED
==========================================================================================



Procedures

A procedure is a block of SQL code that performs a
series of operations - like inserting, updating, deleting,
or selecting data - and is stored in the database.
" Think of it like a function in programming - once
defined, you can call it again and again without rewriting
the logic."


* Reusability

  * Write once, use many times.

* Security

  * Logic is stored in DB, no need to give direct access to all tables.

* Faster Execution

  * Compiled and stored on the DB server.

* Encapsulation

  * Hide complex logic in one callable block.

* Multi-step Operations

  * Perform multiple queries like insert + update + log creation in one procedure.












===================================================
Syntax : 


CREATE PROCEDURE procedure_name(param1 datatype,
param2 datatype)
LANGUAGE plpgsql
AS $$
BEGIN
--  SQL logic here
END;
$$;

CALL procedure_name(value1, value2);



===================================

SELECT * FROM flipkart_db;


CREATE OR REPLACE PROCEDURE increase_price()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE flipkart_db
    SET price_max = price_max + 100;
END;
$$;


CALL increase_price();


SELECT product_name, price_max
FROM flipkart_db;