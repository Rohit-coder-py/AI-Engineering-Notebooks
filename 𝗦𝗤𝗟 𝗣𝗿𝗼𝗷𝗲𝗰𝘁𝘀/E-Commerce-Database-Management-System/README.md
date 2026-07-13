# E-Commerce Database Management System

A PostgreSQL database project modeling the core operations of an online store:
customers, product catalog, inventory, orders, payments, shipping, and reviews.
Built to practice relational schema design, constraints, joins, aggregate
reporting, and views on realistic, related data.

## Highlights

- **9 tables** covering the full order lifecycle, from catalog to delivery
- **100 customers · 200 products · 300 orders · 700 order items · 500 reviews**
  of interlinked sample data
- **28 business queries** answering real questions (revenue, top customers,
  low stock, delivery time, ratings, etc.)
- **7 reporting views** for repeatable dashboards
- Enforced data integrity via foreign keys and `CHECK` constraints throughout

## Project Structure

```
E-Commerce-Database-Management-System/
├── database/
│   ├── 01_create_database.sql      # Creates the database
│   ├── 02_create_tables.sql        # Full schema: 9 tables, constraints, FKs
│   ├── 03_insert_sample_data.sql   # Sample data (100 customers ... 500 reviews)
│   ├── 04_queries.sql              # 28 business queries, grouped by table
│   └── 05_views.sql                # 7 reusable reporting views
├── diagrams/
│   ├── er_diagram.png              # Entity-relationship diagram
│   └── schema.png                  # High-level schema overview
├── screenshots/
│   ├── tables.png
│   ├── joins.png
│   ├── views.png
│   ├── revenue_report.png
│   ├── top_customers.png
│   └── inventory_report.png
├── docs/
│   ├── database_design.md          # Design notes and table-by-table rationale
│   └── project_report.pdf          # Written project report
└── README.md
```

## Schema at a Glance

| Table          | Purpose                                            |
|----------------|-----------------------------------------------------|
| `customers`    | Customer profile and contact/location details       |
| `categories`   | Product categories                                   |
| `products`     | Catalog items, priced and linked to a category        |
| `inventory`    | One-to-one stock record per product                    |
| `orders`       | An order placed by a customer                           |
| `order_items`  | Line items on an order (product + quantity)              |
| `payments`     | One-to-one payment record per order                      |
| `shipping`     | One-to-one shipping/delivery record per order              |
| `reviews`      | Customer reviews of products                                |

See [`diagrams/er_diagram.png`](diagrams/er_diagram.png) for the full entity
relationship diagram, and [`docs/database_design.md`](docs/database_design.md)
for the reasoning behind each design decision.

## Getting Started

Requires PostgreSQL (tested on PostgreSQL 13+).

```bash
# 1. Create the database
psql -U <user> -f database/01_create_database.sql

# 2. Create the schema
psql -U <user> -d ecommerce_db -f database/02_create_tables.sql

# 3. Load sample data
psql -U <user> -d ecommerce_db -f database/03_insert_sample_data.sql

# 4. Run the business queries
psql -U <user> -d ecommerce_db -f database/04_queries.sql

# 5. Create the reporting views
psql -U <user> -d ecommerce_db -f database/05_views.sql
```

Or from inside `psql`:

```sql
\i database/01_create_database.sql
\c ecommerce_db
\i database/02_create_tables.sql
\i database/03_insert_sample_data.sql
\i database/04_queries.sql
\i database/05_views.sql
```

## Example Queries

Top 10 customers by lifetime spend:

```sql
SELECT c.customer_id, c.first_name, c.last_name,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 10;
```

Products that need restocking:

```sql
SELECT p.product_name, i.stock_quantity, i.reorder_level
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity ASC;
```

More in [`database/04_queries.sql`](database/04_queries.sql), and ready-made
views for the same kind of reporting in [`database/05_views.sql`](database/05_views.sql).

## Design Notes

- `orders`, `payments`, and `shipping` are deliberately split into three
  tables even though each order has exactly one payment and one shipment —
  this keeps each table focused on a single concern and mirrors how a real
  system would evolve (e.g. multiple payment attempts per order later).
- `inventory` is separated from `products` so that stock levels can be
  updated frequently without touching catalog data.
- All monetary values use `NUMERIC(10,2)` to avoid floating-point rounding
  errors.
- Every status column (`order_status`, `payment_status`, `shipping_status`,
  `products.status`) is constrained with `CHECK (... IN (...))` so invalid
  states can't be inserted.

## License

Sample/educational project — free to use and adapt.
