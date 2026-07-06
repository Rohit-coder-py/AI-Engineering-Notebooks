-- String functions in PostgreSQL are used to manipulate text data -
-- like names, categories, SKUs, etc.


SELECT REPEAT('*', 1000);


--  Upper() Convert text to uppercase


Select * from flipkart_db;


Select UPPER(product_name) from flipkart_db;


-- LOWER()	Convert text to lowercase

Select LOWER(product_name) from flipkart_db;


-- LENGTH()	Count the number of characters

Select LENGTH(product_name) from flipkart_db;


-- TRIM()	Remove spaces from both ends

Select TRIM(product_name) from flipkart_db;



-- SUBSTRINGS  Extract part of a string


Select substring('Heyy_letscodee',1,6) ;


Select substring(product_name,1,2),skucode from flipkart_db;



-- Left() and Right()  Return characters from the left and right



Select left('Heyy_letscodee',5)


Select right('Heyy_letscodee',5)




