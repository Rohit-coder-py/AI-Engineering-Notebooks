# SQL JOIN Types Cheat Sheet

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Join Type   Syntax                                                                                                  What it Returns   When to Use     Real-World Use Case
  ----------- ------------------------------------------------------------------------------------------------------- ----------------- --------------- ---------------------
  **INNER     `SELECT * FROM table1 INNER JOIN table2 ON table1.column = table2.column;`                              Only the rows     When you only   Show customers who
  JOIN**                                                                                                              that have         need records    have placed orders,
                                                                                                                      matching values   that exist in   products that have
                                                                                                                      in both tables.   both tables.    been sold, employees
                                                                                                                                                        assigned to a
                                                                                                                                                        department.

  **LEFT JOIN `SELECT * FROM table1 LEFT JOIN table2 ON table1.column = table2.column;`                               All rows from the When the left   Show all products,
  (LEFT OUTER                                                                                                         left table and    table is more   even those that have
  JOIN)**                                                                                                             matching rows     important and   never been ordered.
                                                                                                                      from the right    you don't want  Show all employees,
                                                                                                                      table. If no      to lose any of  even if they are not
                                                                                                                      match exists, the its records.    assigned to a
                                                                                                                      right table                       project.
                                                                                                                      columns contain                   
                                                                                                                      `NULL`.                           

  **RIGHT     `SELECT * FROM table1 RIGHT JOIN table2 ON table1.column = table2.column;`                              All rows from the When the right  Show all orders, even
  JOIN (RIGHT                                                                                                         right table and   table is more   if the product record
  OUTER                                                                                                               matching rows     important and   has been deleted.
  JOIN)**                                                                                                             from the left     you want every  Show all departments,
                                                                                                                      table. If no      record from it. even if no employees
                                                                                                                      match exists, the (Less commonly  work there.
                                                                                                                      left table        used because    
                                                                                                                      columns contain   LEFT JOIN is    
                                                                                                                      `NULL`.           usually         
                                                                                                                                        preferred.)     

  **FULL JOIN `SELECT * FROM table1 FULL JOIN table2 ON table1.column = table2.column;`                               All rows from     When you need   Find unmatched
  (FULL OUTER                                                                                                         both tables.      every record    customers and
  JOIN)**                                                                                                             Matching rows are from both       unmatched orders.
                                                                                                                      combined;         tables,         Compare two datasets
                                                                                                                      non-matching rows regardless of   to identify missing
                                                                                                                      show `NULL` for   whether a match records.
                                                                                                                      missing values.   exists.         

  **CROSS     `SELECT * FROM table1 CROSS JOIN table2;`                                                               Every row from    When you        Generate all
  JOIN**                                                                                                              the first table   intentionally   student-course
                                                                                                                      is combined with  want every      combinations, all
                                                                                                                      every row from    possible        color-size
                                                                                                                      the second table  combination of  combinations for
                                                                                                                      (Cartesian        two tables.     products, all
                                                                                                                      Product).                         possible test cases.

  **SELF      `SELECT a.column, b.column FROM table_name a JOIN table_name b ON a.common_column = b.common_column;`   Joins a table     When related    Employee-Manager
  JOIN**                                                                                                              with itself using information     relationships,
                                                                                                                      aliases.          exists within   category-parent
                                                                                                                                        the same table. category hierarchy,
                                                                                                                                                        family tree
                                                                                                                                                        relationships.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Quick Decision Guide

  Situation                               Join to Use
  --------------------------------------- --------------
  Need only matching records              `INNER JOIN`
  Need all records from the left table    `LEFT JOIN`
  Need all records from the right table   `RIGHT JOIN`
  Need every record from both tables      `FULL JOIN`
  Need every possible combination         `CROSS JOIN`
  Need to join a table with itself        `SELF JOIN`

------------------------------------------------------------------------

# SQL Join Cheat Sheet

  ---------------------------------------------------------------------------
  Join    Keeps All Left  Keeps All Right  Requires     Returns `NULL` for
               Rows            Rows          Match         Missing Data
  ------- --------------- --------------- ----------- -----------------------
  INNER         ❌              ❌            ✅                ❌
  JOIN                                                

  LEFT          ✅              ❌            ❌            Right Table
  JOIN                                                

  RIGHT         ❌              ✅            ❌            Left Table
  JOIN                                                

  FULL          ✅              ✅            ❌            Both Tables
  JOIN                                                

  CROSS         N/A             N/A           ❌                ❌
  JOIN                                                

  SELF    Depends on Join Depends on Join Depends on   Depends on Join Type
  JOIN         Type            Type        Join Type  
  ---------------------------------------------------------------------------
