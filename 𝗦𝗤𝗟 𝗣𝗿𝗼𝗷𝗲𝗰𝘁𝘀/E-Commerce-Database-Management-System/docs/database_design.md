# Database Design

## Overview

`ecommerce_db` models a single online store: a catalog of products organized
into categories, customers who place orders, and everything that happens
after an order is placed — line items, payment, and shipping — plus product
reviews. The design favors normalization (3NF) with a handful of pragmatic
one-to-one splits described below.

See [`diagrams/er_diagram.png`](../diagrams/er_diagram.png) for the full
entity-relationship diagram and [`diagrams/schema.png`](../diagrams/schema.png)
for a grouped, high-level view of how the tables relate.

## Tables

### customers
Core identity and contact data for a shopper. `email` and `phone` are unique.
`gender` is constrained to a small enum via `CHECK`. `created_at` defaults to
the insert time so account age can be derived without extra bookkeeping.

### categories
A flat list of product categories (Electronics, Fashion, Books, ...).
Kept as its own table rather than a free-text column on `products` so
category names stay consistent and can be renamed in one place.

### products
The catalog. Each product belongs to exactly one category (`fk_product_category`)
and carries its own `price`, `brand`, and lifecycle `status`
(`Available` / `Out of Stock` / `Discontinued`). `price` uses
`NUMERIC(10,2)` — not `FLOAT` — so currency values never suffer
floating-point rounding drift.

### inventory
Deliberately separated from `products` in a strict 1:1 relationship
(`product_id` is `UNIQUE`). Stock counts change far more often than catalog
data (name, description, brand), so keeping them in different tables avoids
unnecessary writes to `products` on every sale and makes it easy to
audit/index inventory movement independently. `reorder_level` drives the
low-stock queries and the `inventory_alert` view.

### orders
One row per order placed by a customer. `order_status` is constrained to
`Pending → Processing → Shipped → Delivered` (or `Cancelled`) so the
application layer can trust the value without extra validation.
`total_amount` is stored on the order itself (denormalized) rather than
always summed from `order_items`, which is a common, deliberate trade-off
in order systems: it captures the amount actually charged at checkout time,
even if line items or prices are edited later.

### order_items
The many-to-many bridge between `orders` and `products`, with `quantity`
and the `unit_price` captured **at the time of purchase**. Storing
`unit_price` here (rather than joining back to `products.price`) protects
historical order data from later price changes — if a product's price
changes next month, past invoices stay accurate.

### payments
One payment record per order (`order_id` is `UNIQUE`), covering method
(`UPI`, `Credit Card`, `Debit Card`, `Net Banking`, `Cash on Delivery`) and
status (`Pending`, `Paid`, `Failed`, `Refunded`). Kept separate from `orders`
so payment retries/refund logic can evolve without widening the `orders`
table, and so a future multi-payment-attempt model is a small schema change
rather than a rewrite.

### shipping
One shipping record per order (`order_id` is `UNIQUE`), holding delivery
address, dates, and status (`Preparing`, `Shipped`, `In Transit`,
`Delivered`). Split from `orders` for the same reason as `payments` — a
single order can conceptually have shipment tracking added, changed, or
extended without touching the order record itself.

### reviews
Customer feedback on a product, with a `rating` between 1 and 5. A review is
linked to a customer and a product but not to a specific order — this keeps
the schema simple while still supporting all common review queries
(average rating per product, most-reviewed products, low-rated products).

## Relationships Summary

| From          | To            | Cardinality | Enforced by                  |
|---------------|---------------|-------------|-------------------------------|
| customers     | orders        | 1 : N       | `orders.customer_id`          |
| customers     | reviews       | 1 : N       | `reviews.customer_id`         |
| categories    | products      | 1 : N       | `products.category_id`        |
| products      | inventory     | 1 : 1       | `inventory.product_id` UNIQUE |
| products      | order_items   | 1 : N       | `order_items.product_id`      |
| products      | reviews       | 1 : N       | `reviews.product_id`          |
| orders        | order_items   | 1 : N       | `order_items.order_id`, `ON DELETE CASCADE` |
| orders        | payments      | 1 : 1       | `payments.order_id` UNIQUE    |
| orders        | shipping      | 1 : 1       | `shipping.order_id` UNIQUE    |

`order_items.order_id` cascades on delete: removing an order removes its
line items with it, since a line item has no meaning without its parent
order. No other foreign key cascades — deleting a customer, product, or
category is left as an explicit decision for the application layer, since
those deletions have knock-on effects (order history, reviews) that
shouldn't happen silently.

## Constraints & Data Integrity

- Every monetary column (`price`, `total_amount`, `unit_price`, `amount`)
  has a `CHECK` ensuring it is positive (or non-negative for totals).
- `quantity`, `stock_quantity`, and `rating` all have range checks.
- Every status/enum-like column (`gender`, `order_status`, `payment_status`,
  `payment_method`, `shipping_status`, `products.status`) is constrained
  with `CHECK (... IN (...))`.
- Foreign keys enforce that an `order_item`, `payment`, or `shipping` record
  can't exist without a valid parent `order`, and a `product` can't exist
  without a valid `category`.

## Reporting Layer

Rather than repeating the same joins in every query, seven views in
[`database/05_views.sql`](../database/05_views.sql) pre-package the most
common reporting shapes:

- `order_summary` — one row per order with customer, payment, and shipping status
- `product_catalog` — products joined with category and live stock status
- `inventory_alert` — products at or below their reorder level
- `customer_spending` — lifetime order count and spend per customer
- `monthly_revenue` — revenue and order volume by month
- `product_ratings` — average rating and review count per product
- `all_joined` — a fully denormalized export across every table

## Sample Data

`03_insert_sample_data.sql` seeds a self-consistent dataset: 10 categories,
100 customers, 200 products, matching inventory rows for every product, 300
orders (each with a payment and shipping record), 700 order line items, and
500 reviews — enough volume to make aggregate queries (top customers,
monthly revenue, low stock) meaningful rather than trivial.
