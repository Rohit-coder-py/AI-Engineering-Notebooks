# SQL CRUD Operations

## CREATE (INSERT)

```sql
INSERT INTO table_name(column1, column2, ...)
VALUES(value1, value2, ...);
```

---

## READ (SELECT)

```sql
SELECT * FROM table_name;
```

```sql
SELECT column1, column2
FROM table_name;
```

---

## UPDATE

```sql
UPDATE table_name
SET column_name = value
WHERE condition;
```

---

## DELETE

```sql
DELETE FROM table_name
WHERE condition;
```

> **⚠️ Always use `WHERE` with `UPDATE` and `DELETE` unless you want to modify/delete all rows.**