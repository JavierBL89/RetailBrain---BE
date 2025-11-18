
# Run from terminal
Enter the Postgres shell:

 - docker exec -it retailbrain---be-db-1 psql -U hackathon_user -d mydatabase

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
