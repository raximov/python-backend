-- =====================================================
-- Store API - PostgreSQL Database Schema
-- =====================================================
-- This script creates the database and tables required 
-- for the Store API application.
-- 
-- Usage:
--   psql -U postgres -f init_db.sql
-- =====================================================

-- Create database (uncomment if you have permissions)
-- CREATE DATABASE store_api;
-- \c store_api;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- Table: addresses
-- Shared address entity for clients and suppliers
-- =====================================================
CREATE TABLE IF NOT EXISTS addresses (
    id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    country     VARCHAR(100)  NOT NULL,
    city        VARCHAR(100)  NOT NULL,
    street      VARCHAR(255)  NOT NULL
);

-- =====================================================
-- Table: images
-- Stores product images as binary data (bytea)
-- =====================================================
CREATE TABLE IF NOT EXISTS images (
    id          VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    image       BYTEA         NOT NULL
);

-- =====================================================
-- Table: suppliers
-- Supplier entity with FK to addresses
-- =====================================================
CREATE TABLE IF NOT EXISTS suppliers (
    id              VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    name            VARCHAR(150)  NOT NULL,
    address_id      VARCHAR(36)   REFERENCES addresses(id) ON DELETE SET NULL,
    phone_number    VARCHAR(20)
);

-- =====================================================
-- Table: products
-- Product entity with FKs to suppliers and images
-- =====================================================
CREATE TABLE IF NOT EXISTS products (
    id                  VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    name                VARCHAR(200)  NOT NULL,
    category            VARCHAR(100)  NOT NULL,
    price               DOUBLE PRECISION NOT NULL CHECK (price >= 0),
    available_stock     INTEGER       NOT NULL DEFAULT 0 CHECK (available_stock >= 0),
    last_update_date    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    supplier_id         VARCHAR(36)   REFERENCES suppliers(id) ON DELETE SET NULL,
    image_id            VARCHAR(36)   REFERENCES images(id) ON DELETE SET NULL
);

-- =====================================================
-- Table: clients
-- Client entity with FK to addresses
-- =====================================================
CREATE TABLE IF NOT EXISTS clients (
    id                  VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    client_name         VARCHAR(100)  NOT NULL,
    client_surname      VARCHAR(100)  NOT NULL,
    birthday            DATE,
    gender              VARCHAR(10)   CHECK (gender IN ('male', 'female', 'other')),
    registration_date   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    address_id          VARCHAR(36)   REFERENCES addresses(id) ON DELETE SET NULL
);

-- =====================================================
-- Indexes for common queries
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_clients_name 
    ON clients(client_name, client_surname);

CREATE INDEX IF NOT EXISTS idx_products_available 
    ON products(available_stock) WHERE available_stock > 0;

CREATE INDEX IF NOT EXISTS idx_products_supplier 
    ON products(supplier_id);

CREATE INDEX IF NOT EXISTS idx_products_image 
    ON products(image_id);
