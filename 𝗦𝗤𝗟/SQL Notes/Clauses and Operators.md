# SQL Clauses :

| Clause | Syntax | Description |
|--------|--------|-------------|
| **SELECT** | `SELECT column1, column2 FROM table_name;` | Choose which columns to display |
| **FROM** | `SELECT * FROM table_name;` | Specify the table |
| **WHERE** | `SELECT * FROM table_name WHERE condition;` | Filter rows based on a condition |
| **GROUP BY** | `SELECT column, AGG_FUNC(column) FROM table_name GROUP BY column;` | Group rows for aggregation |
| **HAVING** | `SELECT column, AGG_FUNC(column) FROM table_name GROUP BY column HAVING condition;` | Filter aggregated groups (used after `GROUP BY`) |
| **ORDER BY** | `SELECT * FROM table_name ORDER BY column ASC/DESC;` | Sort the result in ascending or descending order |
| **LIMIT** | `SELECT * FROM table_name LIMIT number;` | Limit the number of rows returned |
| **AS** | `SELECT column AS alias FROM table_name;` | Rename columns or tables temporarily (aliasing) |
| **DISTINCT** | `SELECT DISTINCT column FROM table_name;` | Return only unique/distinct values |