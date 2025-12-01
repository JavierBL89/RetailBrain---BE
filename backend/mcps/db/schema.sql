-- ============================================
--  DATABASE SCHEMA FOR RETAILBRAIN
-- ============================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABLE: products
-- ============================================

CREATE TABLE IF NOT EXISTS products (
    product_id     SERIAL PRIMARY KEY,
    sku            VARCHAR(50) NOT NULL,
    name           VARCHAR(250) NOT NULL,
    category       VARCHAR(100),
    brand          VARCHAR(50),
    gender       VARCHAR(25),
    created_at     TIMESTAMP DEFAULT NOW(),
    updated_at     TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLE: tags
-- ============================================

CREATE TABLE IF NOT EXISTS tags (
    tag_id     SERIAL PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL
);

-- ============================================
-- TABLE: product_tags (many-to-many)
-- ============================================

CREATE TABLE IF NOT EXISTS product_tags (
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    tag_id     INTEGER NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, tag_id)
);

-- ============================================
-- TABLE: sizes
-- ============================================

CREATE TABLE IF NOT EXISTS sizes (
    size_id     SERIAL PRIMARY KEY,
    size_label  VARCHAR(10) UNIQUE NOT NULL
);

-- ============================================
-- TABLE: product_variants
-- ============================================

CREATE TABLE IF NOT EXISTS product_variants (
    variant_id   SERIAL PRIMARY KEY,
    product_id   INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    variant_sku  VARCHAR(50) NOT NULL,
    name           VARCHAR(250) NOT NULL,
    description  VARCHAR(500) NOT NULL,
    category       VARCHAR(100),
    color        VARCHAR(50),
    material     VARCHAR(50),
    gender       VARCHAR(25),
    brand          VARCHAR(50),
    price        NUMERIC(10,2) NOT NULL,
    image_url    TEXT,
    tags_string  TEXT,
    created_at   TIMESTAMP DEFAULT NOW(),
    updated_at   TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLE: variant_sizes (stock matrix)
-- ============================================

CREATE TABLE IF NOT EXISTS variant_sizes (
    variant_id      INTEGER NOT NULL REFERENCES product_variants(variant_id) ON DELETE CASCADE,
    size_id         INTEGER NOT NULL REFERENCES sizes(size_id) ON DELETE CASCADE,
    stock_quantity  INTEGER NOT NULL DEFAULT 0,
    available       BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (variant_id, size_id)
);


-- ============================================
-- Product Variant metadata
-- ============================================
CREATE TABLE IF NOT EXISTS variant_metadata (
    metadata_id SERIAL PRIMARY KEY,
    variant_id INTEGER NOT NULL UNIQUE REFERENCES product_variants(variant_id) ON DELETE CASCADE,

    brand TEXT,
    category TEXT,
    color TEXT,
    material TEXT,
    heel_type TEXT,
    heel_height TEXT,
    tags_string TEXT,
    occasion TEXT,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);



-- ============================================
-- TABLE: sales
-- ============================================

CREATE TABLE IF NOT EXISTS sales (
    sale_id        SERIAL PRIMARY KEY,
    customer_city  VARCHAR(255),
    payment_method VARCHAR(100),
    sale_date      TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLE: sale_line_item
-- ============================================

CREATE TABLE IF NOT EXISTS sale_line_item (
    line_item_id SERIAL PRIMARY KEY,
    sale_id      INTEGER NOT NULL REFERENCES sales(sale_id) ON DELETE CASCADE,
    variant_id   INTEGER NOT NULL REFERENCES product_variants(variant_id) ON DELETE CASCADE,
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    unit_price   NUMERIC(10,2) NOT NULL
);

-- ============================================
-- TABLE: sale_line_item
-- ============================================
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL
);

-- ============================================
-- TABLE: sale_line_item
-- ============================================
CREATE TABLE payment_methods (
    method_id SERIAL PRIMARY KEY,
    method_name TEXT NOT NULL UNIQUE
);