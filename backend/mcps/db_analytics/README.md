# SHUT DOWN DB

 - docker compose down
 - docker compose up --build

# BUILD DATABASE

1. Start docker if not running

  - docker-compose up -d

2. List containers running. Ensure db container is running
  
  - docker ps
 
5. Verify tables 

  - docker exec -it db psql -U hackathon_user -d mydatabase -c "\dt"


# Run from terminal
Enter the Postgres shell:

 - docker exec -it db psql -U hackathon_user -d mydatabase


### Fetch a full product with variants:
SELECT 
    p.product_id,
    p.name,
    v.variant_sku,
    v.color,
    v.price,
    v.image_url
FROM products p
JOIN product_variants v ON v.product_id = p.product_id
WHERE p.product_id = 9;   -- replace with any ID from your list



# Verify tables

# 1. Check products (should be 15)
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT COUNT(*) FROM products;"

# 2. Check product_variants with auto-generated IDs (should be 15)
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT variant_id, product_id, variant_sku, color, price FROM product_variants ORDER BY variant_id;"

# 3. Check sizes (should be 6)
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT * FROM sizes;"

# 4. Check variant_sizes matrix (should be 90: 15 variants × 6 sizes)
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT COUNT(*) FROM variant_sizes;"

# 6. Check sales table count
docker exec -it db psql -U hackathon_user -d mydatabase -c "SELECT COUNT(*) FROM sales;"


# 7. Sales analysis by month
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    TO_CHAR(sale_date, 'YYYY-MM') as month,
    COUNT(*) as sales_count,
    ROUND(SUM(sli.quantity * sli.unit_price), 2) as total_revenue
FROM sales s
JOIN sale_line_item sli ON s.sale_id = sli.sale_id
GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
ORDER BY month;
"

# 8. Top selling products
docker exec -it db psql -U hackathon_user -d mydatabase -c "
SELECT 
    p.name,
    v.color,
    SUM(sli.quantity) as total_sold,
    ROUND(SUM(sli.quantity * sli.unit_price), 2) as revenue
FROM sale_line_item sli
JOIN product_variants v ON sli.variant_id = v.variant_id
JOIN products p ON v.product_id = p.product_id
GROUP BY p.name, v.color
ORDER BY total_sold DESC
LIMIT 10;
"

# 9. Revenue trends
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

# 10. Test a complete query to see product with all its variants and sizes
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



## Rebuild database entirely -> seed.sql file  (this will remove any data and reenter data in seed.sql file)
     - ./backend/mcps/db_analytics/db/schema.sql:/docker-entrypoint-initdb.d/00-schema.sql
      - ./backend/mcps/db_analytics/db/seed.sql:/docker-entrypoint-initdb.d/01-seed.sql