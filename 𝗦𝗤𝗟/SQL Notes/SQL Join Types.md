# | Join Type | Syntax | What it Returns | When to Use |

# |-----------|--------|-----------------|-------------|

# | \*\*INNER JOIN\*\* | `SELECT \* FROM table1 INNER JOIN table2 ON table1.column = table2.column;` | Only the rows that have matching values in both tables. | When you only need records that exist in both tables. |

# | \*\*LEFT JOIN (LEFT OUTER JOIN)\*\* | `SELECT \* FROM table1 LEFT JOIN table2 ON table1.column = table2.column;` | All rows from the left table and matching rows from the right table. If no match exists, the right table columns contain `NULL`. | When the left table is more important and you don't want to lose any of its records. |

# | \*\*RIGHT JOIN (RIGHT OUTER JOIN)\*\* | `SELECT \* FROM table1 RIGHT JOIN table2 ON table1.column = table2.column;` | All rows from the right table and matching rows from the left table. If no match exists, the left table columns contain `NULL`. | When the right table is more important and you want every record from it. (Less commonly used because LEFT JOIN is usually preferred.) |

# | \*\*FULL JOIN (FULL OUTER JOIN)\*\* | `SELECT \* FROM table1 FULL JOIN table2 ON table1.column = table2.column;` | All rows from both tables. Matching rows are combined; non-matching rows show `NULL` for missing values. | When you need every record from both tables, regardless of whether a match exists. |

# | \*\*CROSS JOIN\*\* | `SELECT \* FROM table1 CROSS JOIN table2;` | Every row from the first table is combined with every row from the second table (Cartesian Product). | When you intentionally want every possible combination of two tables. |

# | \*\*SELF JOIN\*\* | `SELECT a.column, b.column FROM table\_name a JOIN table\_name b ON a.common\_column = b.common\_column;` | Joins a table with itself using aliases. | When related information exists within the same table. |

