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

# 5. Test a complete query to see product with all its variants and sizes
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