
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    date_of_birth DATE,
    gender VARCHAR(10) CHECK (gender IN ('Male','Female','Other')),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- =========================
-- Products
-- =========================
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category_id INT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    description TEXT,
    brand VARCHAR(100),
    price NUMERIC(10,2) NOT NULL CHECK (price > 0),
    status VARCHAR(20) DEFAULT 'Available'
        CHECK (status IN ('Available','Out of Stock','Discontinued')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

-- =========================
-- Inventory
-- =========================
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0),
    reorder_level INT DEFAULT 10,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- =========================
-- Orders
-- =========================
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(20)
        DEFAULT 'Pending'
        CHECK (order_status IN
        ('Pending','Processing','Shipped','Delivered','Cancelled')),
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount >= 0),

    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

-- =========================
-- Order Items
-- =========================
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price > 0),

    CONSTRAINT fk_item_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_item_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- =========================
-- Payments
-- =========================
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT UNIQUE NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(30)
        CHECK (payment_method IN
        ('UPI','Credit Card','Debit Card','Net Banking','Cash on Delivery')),
    payment_status VARCHAR(20)
        DEFAULT 'Pending'
        CHECK (payment_status IN
        ('Pending','Paid','Failed','Refunded')),
    amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),

    CONSTRAINT fk_payment_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

-- =========================
-- Shipping
-- =========================
CREATE TABLE shipping (
    shipping_id SERIAL PRIMARY KEY,
    order_id INT UNIQUE NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(15),
    shipping_date DATE,
    delivery_date DATE,
    shipping_status VARCHAR(20)
        DEFAULT 'Preparing'
        CHECK (shipping_status IN
        ('Preparing','Shipped','In Transit','Delivered')),

    CONSTRAINT fk_shipping_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

-- =========================
-- Reviews
-- =========================
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_review_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

