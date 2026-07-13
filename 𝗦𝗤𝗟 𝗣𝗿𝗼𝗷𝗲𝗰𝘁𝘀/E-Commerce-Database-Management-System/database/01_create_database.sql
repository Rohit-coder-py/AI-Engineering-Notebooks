-- =========================================================
-- E-Commerce Database Management System
-- 01_create_database.sql
-- Creates the database and switches into it.
-- =========================================================

CREATE DATABASE ecommerce_db;

-- Run the remaining scripts against this database, in order:
--   psql -U <user> -d ecommerce_db -f 02_create_tables.sql
--   psql -U <user> -d ecommerce_db -f 03_insert_sample_data.sql
--   psql -U <user> -d ecommerce_db -f 04_queries.sql
--   psql -U <user> -d ecommerce_db -f 05_views.sql
--
-- Or, if you are already connected via psql:
--   \c ecommerce_db
