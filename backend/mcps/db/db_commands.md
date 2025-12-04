## Key Features of the data inserted:
**~1000 Sales distributed across 6 months with:**
    May 2025: 140 sales (spring baseline)
    June 2025: 150 sales (summer starts)
    July 2025: 180 sales (peak summer + July 4th spike)
    August 2025: 170 sales (back-to-school season)
    September 2025: 160 sales (fall season)
    October 2025: 170 sales (Halloween spike)
    November 2025: 200 sales (Black Friday boost)
**Realistic Patterns:**
    Higher sales on weekends (6-8 sales/day vs 4-5 weekdays)
    Seasonal spikes (July 4th, back-to-school, Black Friday)
    70% of sales focus on popular variants (1, 3, 7, 11, 14)
    80% single-item purchases, 15% two items, 5% three items
    Black Friday discounts (10-20% off in mid-November)
    Multiple payment methods and locations across 27 US cities



## 📦 Product Catalog Reference

### Available Products (Product IDs 9-23)

1. **MJ Wedge Shoe** (ID: 9, 16) - Black & Brown variants
2. **Mary Jane Patent Shoe** (ID: 10) - Black
3. **Studded Peep Toe** (ID: 11) - Red/Brown/Gold
4. **Ankle Boot** (ID: 12) - Black
5. **Metallic Heel Shoe** (ID: 13) - Black
6. **Platform Sandal** (ID: 14) - Orange
7. **Embellished Peep Toe** (ID: 15) - Red
8. **Stud Clear Shoe** (ID: 17) - Black
9. **Clear Wedge Gold** (ID: 18) - Gold/Clear
10. **Comfort 3 Shoe** (ID: 19, 20) - Beige & Black
11. **High Top Boot** (ID: 21) - Brown
12. **Riding Boot** (ID: 22, 23) - Black & Cognac

### Price Range
- **Budget**: $34.50 - $42.00 (Wedges, Comfort shoes)
- **Mid-Range**: $59.00 - $99.00 (Most products)
- **Premium**: $119.00 - $129.00 (Boots)


## 🔍 Essential Query Commands

### 1. **Quick Data Verification**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
  'products' as table_name, COUNT(*) as count FROM products
UNION ALL
SELECT 'product_variants', COUNT(*) FROM product_variants
UNION ALL
SELECT 'sizes', COUNT(*) FROM sizes
UNION ALL
SELECT 'variant_sizes', COUNT(*) FROM variant_sizes
UNION ALL
SELECT 'sales', COUNT(*) FROM sales
UNION ALL
SELECT 'sale_line_item', COUNT(*) FROM sale_line_item;
"
```

**Expected Output:**
- products: 15
- product_variants: 15
- sizes: 6
- variant_sizes: 90
- sales: ~1,065
- sale_line_item: ~1,200-1,500




# 1. Product Performance

**Sales by product category and month:**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    p.category,
    TO_CHAR(s.sale_date, 'YYYY-MM') as month,
    COUNT(*) as sales_count,
    SUM(sli.quantity) as units_sold,
    ROUND(SUM(sli.quantity * sli.unit_price), 2) as revenue
FROM sales s
JOIN sale_line_item sli ON s.sale_id = sli.sale_id
JOIN product_variants v ON sli.variant_id = v.variant_id
JOIN products p ON v.product_id = p.product_id
GROUP BY p.category, TO_CHAR(s.sale_date, 'YYYY-MM')
ORDER BY month, revenue DESC;
"
```

# 2. Revenue 

**Revenue trends**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    TO_CHAR(sale_date, '2025-06') as month,
    COUNT(DISTINCT s.sale_id) as num_orders,
    ROUND(AVG(order_totals.total), 2) as avg_order_value,
    ROUND(SUM(order_totals.total), 2) as monthly_revenue
FROM sales s
JOIN (
    SELECT sale_id, SUM(quantity * unit_price) as total
    FROM sale_line_item
    GROUP BY sale_id
) order_totals ON s.sale_id = order_totals.sale_id
GROUP BY TO_CHAR(sale_date, '2025-06')
ORDER BY month;
"
```

**Revenue trends & KPIs**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    TO_CHAR(sale_date, 'YYYY-MM') as month,
    COUNT(DISTINCT s.sale_id) as num_orders,
    SUM(sli.quantity) as total_items_sold,
    ROUND(AVG(order_totals.total), 2) as avg_order_value,
    ROUND(SUM(order_totals.total), 2) as monthly_revenue
FROM sales s
JOIN sale_line_item sli ON s.sale_id = sli.sale_id
JOIN (
    SELECT sale_id, SUM(quantity * unit_price) as total
    FROM sale_line_item
    GROUP BY sale_id
) order_totals ON s.sale_id = order_totals.sale_id
GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
ORDER BY month;
"
```


# 2. Sales


**Sales analysis by month**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    TO_CHAR(sale_date, '2025-10') as month,
    COUNT(*) as sales_count,
    ROUND(SUM(sli.quantity * sli.unit_price), 2) as total_revenue
FROM sales s
JOIN sale_line_item sli ON s.sale_id = sli.sale_id
GROUP BY TO_CHAR(sale_date, '2025-10')
ORDER BY month;
"
```

**Best performers by units sold:**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    p.name,
    v.color,
    v.variant_sku,
    SUM(sli.quantity) as total_units_sold,
    ROUND(SUM(sli.quantity * sli.unit_price), 2) as total_revenue,
    ROUND(AVG(sli.unit_price), 2) as avg_price
FROM sale_line_item sli
JOIN product_variants v ON sli.variant_id = v.variant_id
JOIN products p ON v.product_id = p.product_id
GROUP BY p.name, v.color, v.variant_sku
ORDER BY total_units_sold DESC
LIMIT 10;
"
```

**Sales by day of the week**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    TO_CHAR(sale_date, 'Day') as day_of_week,
    COUNT(*) as sales_count,
    ROUND(AVG(order_totals.total), 2) as avg_order_value
FROM sales s
JOIN (
    SELECT sale_id, SUM(quantity * unit_price) as total
    FROM sale_line_item
    GROUP BY sale_id
) order_totals ON s.sale_id = order_totals.sale_id
GROUP BY TO_CHAR(sale_date, 'Day'), EXTRACT(DOW FROM sale_date)
ORDER BY EXTRACT(DOW FROM sale_date);
"
```

# 3. Products 

**Complete query to see product with all its variants and sizes**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
  p.name,
  v.variant_sku,
  v.color,
  v.price,
  s.size_label,
  vs.stock_quantity,
  vs.available
FROM products p
JOIN product_variants v ON v.product_id = p.product_id
JOIN variant_sizes vs ON vs.variant_id = v.variant_id
JOIN sizes s ON s.size_id = vs.size_id
WHERE p.product_id = 9
ORDER BY s.size_label;
"
```


# 4.Payment Method Distribution 

**Payment preferences:**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    payment_method,
    COUNT(*) as transactions,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM sales
GROUP BY payment_method
ORDER BY transactions DESC;
"
```




-----------------
**Product Update:**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
UPDATE products
SET 
    sku = COALESCE($2, sku),
    category = COALESCE($3, category),
    brand = COALESCE($4, brand)
WHERE product_id = $1;
```


**Product variant Update:**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
UPDATE product_variants
SET
    variant_sku = COALESCE($2, variant_sku),
    name = COALESCE($3, name),
    description = COALESCE($4, description),
    category = COALESCE($5, category),
    color = COALESCE($6, color),
    material = COALESCE($7, material),
    gender = COALESCE($8, gender),
    brand = COALESCE($9, brand),
    price = COALESCE($10, price),
    image_url = COALESCE($11, image_url),
    tags_string = COALESCE($12, tags_string)
WHERE variant_id = $1;
```


**Size Update:**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
UPDATE sizes
SET size_label = COALESCE($2, size_label)
WHERE size_id = $1;
```



**Size variant Update:**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
UPDATE variant_sizes
SET
    stock_quantity = COALESCE($3, stock_quantity),
    available = COALESCE($4, available)
WHERE variant_id = $1 AND size_id = $2;
```


**Delete product** (deletes in cascade the product, all its variants, all variant-size entries)
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
DELETE FROM products
WHERE product_id = $1
RETURNING *;
```


**Delete product variant**
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
DELETE FROM product_variants
WHERE variant_id = $1
RETURNING *;
```

**Dele Size** and all variant-size links
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
DELETE FROM sizes
WHERE size_id = $1
RETURNING *;
```

**Delete variant size** (single size entry)
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "
DELETE FROM variant_sizes
WHERE variant_id = $1 AND size_id = $2
RETURNING *;
```




## 🛠️ Useful Management Commands

### Connect to Database
```bash
docker exec -it db psql -U hackathon_user -d mydatabase
```

### List All Tables
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "\dt"
```

### Check products (should be 15)
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT COUNT(*) FROM products;"
```

### Check product_variants with auto-generated IDs (should be 15)
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT variant_id, product_id, variant_sku, color, price FROM product_variants ORDER BY variant_id;"
```

### Check sizes (should be 6)
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT * FROM sizes;"
```

### Check variant_sizes matrix (should be 90: 15 variants × 6 sizes)
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT COUNT(*) FROM variant_sizes;"
```

### Check sales table count
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT COUNT(*) FROM sales;"
```

## (WARNING) Rebuild database entirely -> seed.sql file  (this will remove any data and reenter data in seed.sql file)
```bash
    - ./backend/mcps/db/schema.sql:/docker-entrypoint-initdb.d/00-schema.sql
    - ./backend/mcps/db_analytics/db/seed.sql:/docker-entrypoint-initdb.d/01-seed.sql
```

### View Table Schema
```bash
docker exec -it db psql -U hackathon_user -d mydatabase -c "\d products"
docker exec -it db psql -U hackathon_user -d mydatabase -c "\d sales"
```

### Reset Containers 
```bash
docker compose down -v
docker compose up --build
```

### Check Container Logs
```bash
docker logs db
docker logs orchestrator
```


---