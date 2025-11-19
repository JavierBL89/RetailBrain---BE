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
**Business Intelligence Ready:**
    Top selling products analysis
    Revenue trends by month
    Average order value tracking
    Customer location patterns
    Payment method preferences
    Seasonal sales patterns


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