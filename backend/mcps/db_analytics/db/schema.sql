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
    name           VARCHAR(255) NOT NULL,
    description    TEXT,
    category       VARCHAR(100),
    material       VARCHAR(100),
    gender         VARCHAR(50),
    brand          VARCHAR(100),
    tags_string    TEXT,
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
    color        VARCHAR(100),
    price        NUMERIC(10,2) NOT NULL,
    image_url    TEXT,
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
-- TABLE: sales
-- ============================================

CREATE TABLE IF NOT EXISTS sales (
    sale_id        SERIAL PRIMARY KEY,
    customer_name  VARCHAR(255),
    location       VARCHAR(100),
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
