# SQL Data Types - Short Notes

## 1) Numeric Data Types

| Data Type | Description | Example |
|-----------|-------------|---------|
| `SMALLINT` | Stores small whole numbers. | `25` |
| `INT` / `INTEGER` | Stores whole numbers. | `100` |
| `BIGINT` | Stores very large whole numbers. | `9876543210` |
| `SERIAL` | Auto-incrementing integer (commonly used for IDs). | `1, 2, 3...` |
| `BIGSERIAL` | Auto-incrementing BIGINT. | `1, 2, 3...` |
| `DECIMAL(p,s)` | Stores exact decimal numbers. | `999.99` |
| `NUMERIC(p,s)` | Same as `DECIMAL`; exact decimal values. | `1250.50` |
| `REAL` | Stores single-precision decimal numbers. | `3.14` |
| `DOUBLE PRECISION` | Stores double-precision decimal numbers. | `3.1415926535` |

---

## 2) Character/String Data Types

| Data Type | Description | Example |
|-----------|-------------|---------|
| `CHAR(n)` | Stores fixed-length text. | `CHAR(5)` |
| `VARCHAR(n)` | Stores variable-length text (max `n` characters). | `VARCHAR(50)` |
| `TEXT` | Stores long text with no practical length limit. | `"This is a long description..."` |
| `UUID` | Stores universally unique identifiers. | `550e8400-e29b...` |
| `JSON` | Stores JSON data. | `{"name":"Harsh"}` |
| `JSONB` | Binary JSON (faster and more efficient than JSON). | `{"age":23}` |
| `BYTEA` | Stores binary data (images, files, etc.). | Binary data |

---

## 3) Boolean Type

| Data Type | Description | Example |
|-----------|-------------|---------|
| `BOOLEAN` | Stores logical values (`TRUE` or `FALSE`). | `TRUE` |

---

## 4) Date and Time Types

| Data Type | Description | Example |
|-----------|-------------|---------|
| `DATE` | Stores date only. | `2026-07-02` |
| `TIME` | Stores time only. | `14:30:45` |
| `TIMESTAMP` | Stores both date and time. | `2026-07-02 14:30:45` |

---

### ⭐ Most Important Data Types for Beginners

| Data Type       | Purpose            |
| --------------- | ------------------ |
| `SERIAL`        | Auto-generated IDs |
| `INT`           | Whole numbers      |
| `VARCHAR(n)`    | Short text         |
| `TEXT`          | Long text          |
| `DECIMAL(10,2)` | Money / Prices     |
| `BOOLEAN`       | True / False       |
| `DATE`          | Date               |
| `TIME`          | Time               |
| `TIMESTAMP`     | Date & Time        |

These are the data types you'll use in **90% of SQL projects**.