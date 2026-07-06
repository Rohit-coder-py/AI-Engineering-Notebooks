# SQL Aggregate Functions

## What are Aggregate Functions?

Aggregate functions perform calculations on **multiple rows** and return
**a single value**.

------------------------------------------------------------------------

## 1. COUNT()

Counts the number of rows.

### Syntax

``` sql
SELECT COUNT(*) FROM employees;
```

Count non-NULL values:

``` sql
SELECT COUNT(email) FROM employees;
```

------------------------------------------------------------------------

## 2. SUM()

Returns the total of a numeric column.

### Syntax

``` sql
SELECT SUM(salary) FROM employees;
```

------------------------------------------------------------------------

## 3. AVG()

Returns the average value.

### Syntax

``` sql
SELECT AVG(salary) FROM employees;
```

------------------------------------------------------------------------

## 4. MIN()

Returns the smallest value.

### Syntax

``` sql
SELECT MIN(salary) FROM employees;
```

------------------------------------------------------------------------

## 5. MAX()

Returns the largest value.

### Syntax

``` sql
SELECT MAX(salary) FROM employees;
```

------------------------------------------------------------------------

# Sample Table

  ID   Name    Department     Salary
  ---- ------- ------------ --------
  1    Harsh   IT              50000
  2    Rahul   HR              60000
  3    Aman    IT              45000
  4    Priya   Sales           80000

------------------------------------------------------------------------

## COUNT()

``` sql
SELECT COUNT(*) AS total_employees
FROM employees;
```

**Output**

    total_employees
  -----------------
                  4

------------------------------------------------------------------------

## SUM()

``` sql
SELECT SUM(salary) AS total_salary
FROM employees;
```

**Output**

    total_salary
  --------------
          235000

------------------------------------------------------------------------

## AVG()

``` sql
SELECT AVG(salary) AS average_salary
FROM employees;
```

**Output**

    average_salary
  ----------------
             58750

------------------------------------------------------------------------

## MIN()

``` sql
SELECT MIN(salary) AS lowest_salary
FROM employees;
```

**Output**

    lowest_salary
  ---------------
            45000

------------------------------------------------------------------------

## MAX()

``` sql
SELECT MAX(salary) AS highest_salary
FROM employees;
```

**Output**

    highest_salary
  ----------------
             80000

------------------------------------------------------------------------

# Aggregate Functions with WHERE

``` sql
SELECT AVG(salary)
FROM employees
WHERE department = 'IT';
```

Only IT employees are considered.

------------------------------------------------------------------------

# Aggregate Functions with GROUP BY

``` sql
SELECT department,
       COUNT(*) AS employees,
       AVG(salary) AS average_salary
FROM employees
GROUP BY department;
```

------------------------------------------------------------------------

# Aggregate Functions with HAVING

``` sql
SELECT department,
       AVG(salary) AS average_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;
```

`HAVING` filters **groups**, while `WHERE` filters **rows**.

------------------------------------------------------------------------

# NULL Behavior

-   `COUNT(*)` counts every row.
-   `COUNT(column)` ignores NULL values.
-   `SUM()`, `AVG()`, `MIN()`, and `MAX()` ignore NULL values.

------------------------------------------------------------------------

# Quick Summary

  Function    Purpose           Returns
  ----------- ----------------- ---------
  `COUNT()`   Count rows        Integer
  `SUM()`     Total of values   Numeric
  `AVG()`     Average value     Numeric
  `MIN()`     Smallest value    Value
  `MAX()`     Largest value     Value

------------------------------------------------------------------------

# Memory Trick

-   **COUNT()** → How many?
-   **SUM()** → Total
-   **AVG()** → Average
-   **MIN()** → Lowest
-   **MAX()** → Highest
