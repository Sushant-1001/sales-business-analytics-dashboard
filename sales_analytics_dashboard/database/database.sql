



-- ============================================
-- SALES & BUSINESS ANALYTICS DASHBOARD
-- Database: sales_analytics_db
-- ============================================

CREATE DATABASE IF NOT EXISTS sales_analytics_db;

USE sales_analytics_db;


-- ============================================
-- 1. USERS TABLE
-- ============================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================
-- 2. CUSTOMERS TABLE
-- ============================================

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'India',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================
-- 3. PRODUCTS TABLE
-- ============================================

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================
-- 4. SALES TABLE
-- ============================================

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT,
    product_id INT,

    sale_date DATE NOT NULL,

    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,

    total_amount DECIMAL(12,2) NOT NULL,

    payment_method VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE SET NULL,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE SET NULL
);


-- ============================================
-- 5. INSERT ADMIN USER
-- ============================================

INSERT INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin');


-- ============================================
-- 6. SAMPLE CUSTOMERS
-- ============================================

INSERT INTO customers
(customer_name, email, phone, city, state, country)
VALUES
('Rahul Sharma', 'rahul@gmail.com', '9876543210', 'Pune', 'Maharashtra', 'India'),
('Priya Patil', 'priya@gmail.com', '9876543211', 'Mumbai', 'Maharashtra', 'India'),
('Amit Kumar', 'amit@gmail.com', '9876543212', 'Delhi', 'Delhi', 'India'),
('Sneha Joshi', 'sneha@gmail.com', '9876543213', 'Bangalore', 'Karnataka', 'India'),
('Vikas More', 'vikas@gmail.com', '9876543214', 'Nashik', 'Maharashtra', 'India');


-- ============================================
-- 7. SAMPLE PRODUCTS
-- ============================================

INSERT INTO products
(product_name, category, price, stock)
VALUES
('Laptop', 'Electronics', 55000.00, 25),
('Smartphone', 'Electronics', 25000.00, 50),
('Headphones', 'Electronics', 2500.00, 100),
('Office Chair', 'Furniture', 8500.00, 30),
('Keyboard', 'Accessories', 1500.00, 80);


-- ============================================
-- 8. SAMPLE SALES
-- ============================================

INSERT INTO sales
(customer_id, product_id, sale_date, quantity, unit_price, total_amount, payment_method)
VALUES
(1, 1, '2026-01-10', 1, 55000.00, 55000.00, 'UPI'),

(2, 2, '2026-01-15', 2, 25000.00, 50000.00, 'Credit Card'),

(3, 3, '2026-02-05', 3, 2500.00, 7500.00, 'Cash'),

(4, 4, '2026-02-20', 2, 8500.00, 17000.00, 'UPI'),

(5, 5, '2026-03-01', 4, 1500.00, 6000.00, 'Debit Card'),

(1, 2, '2026-03-15', 1, 25000.00, 25000.00, 'UPI'),

(2, 1, '2026-04-05', 1, 55000.00, 55000.00, 'Credit Card'),

(3, 3, '2026-04-18', 5, 2500.00, 12500.00, 'Cash'),

(4, 5, '2026-05-10', 3, 1500.00, 4500.00, 'UPI'),

(5, 4, '2026-05-25', 1, 8500.00, 8500.00, 'Debit Card');