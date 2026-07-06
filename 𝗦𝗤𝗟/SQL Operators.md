# SQL Operators Reference

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Category          Operators                                Syntax Example
  ----------------- ---------------------------------------- --------------------------------------------------------------------------------------------------------
  Comparison        `=`, `!=`, `<>`, `>`, `<`, `>=`, `<=`    `SELECT * FROM employees WHERE salary >= 50000;`

  Logical           `AND`, `OR`, `NOT`                       `SELECT * FROM employees WHERE salary > 50000 AND department = 'IT';`

  Range             `BETWEEN`                                `SELECT * FROM employees WHERE salary BETWEEN 40000 AND 70000;`

  Membership        `IN`, `NOT IN`                           `SELECT * FROM employees WHERE department IN ('IT', 'HR');`

  Pattern Matching  `LIKE`, `ILIKE` (PostgreSQL), `NOT LIKE` `SELECT * FROM employees WHERE name LIKE 'A%';`

  Null Checking     `IS NULL`, `IS NOT NULL`                 `SELECT * FROM employees WHERE manager_id IS NULL;`

  Existence (later) `EXISTS`, `NOT EXISTS`                   `SELECT * FROM customers WHERE EXISTS (SELECT 1 FROM orders WHERE customers.id = orders.customer_id);`
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------
