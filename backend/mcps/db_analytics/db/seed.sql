
-- How to run this seed file:
  docker exec -i retailbrain---be-db-1 \
  psql -U hackathon_user -d mydatabase < db/seed.sql

  or ALL at once

  docker compose up -d
  docker exec -i retailbrain---be-db-1 psql -U hackathon_user -d mydatabase < backend/mcps/db_analytics/db/seed.sql

-- =========================================    

-- ========== SIZES ==========
INSERT INTO sizes (size_label)
VALUES ('36'),('37'),('38'),('39'),('40'),('41')
ON CONFLICT (size_label) DO NOTHING;


-- ========== PRODUCT VARIANTS ==========

INSERT INTO product_variants (product_id, variant_sku, color, price, image_url) VALUES
(9,  'MJWEDGE-BLK', 'Black', 34.50, 'MJWEDGE_black.jpg'),
(16, 'MJWEDGE-BRN', 'Brown', 34.50, 'MJWEDGE_brown.jpg'),

(10, 'MJPATENT-BLK', 'Black', 39.99, 'mary_jane_patent_black.jpg'),

(11, 'PEEPSTUD-RED', 'Red/Brown/Gold', 89.99, 'studded_peep_red.jpg'),

(12, 'ANKLBOOT-BLK', 'Black', 119.00, 'ankle_boot_black.jpg'),

(13, 'METSUEDE-BLK', 'Black', 99.00, 'metallic_heel_black.jpg'),

(14, 'PLATSANDL-ORG', 'Orange', 79.50, 'platform_sandal_orange.jpg'),

(15, 'EMBPEEP-RED', 'Red', 94.00, 'embellished_peep_red.jpg'),

-- New batch:
(17, 'STUDCLR-BLK', 'Black', 39.90, '121478.99.jpg'),
(18, 'CLRWEDGE-GLD', 'Gold/Clear', 42.00, '7350693.385.jpg'),
(19, 'COMF3-BEI', 'Beige', 59.00, '101093.342648.jpg'),
(20, 'COMF3-BLK', 'Black', 59.00, '7393158.72.jpg'),
(21, 'HTBOOT-BRN', 'Brown', 129.00, '8049016.60941.jpg'),
(22, 'RIDING-BLK', 'Black', 119.00, '8051626.3.jpg'),
(23, 'RIDING-COG', 'Cognac', 119.00, '8051628.60941.jpg')
ON CONFLICT (variant_sku) DO NOTHING;


-- ========== VARIANT SIZE STOCK MATRIX ==========
INSERT INTO variant_sizes (variant_id, size_id, stock_quantity, available)
SELECT v.variant_id, s.size_id,
       CASE s.size_label
         WHEN '36' THEN 5
         WHEN '37' THEN 8
         WHEN '38' THEN 5
         WHEN '39' THEN 5
         WHEN '40' THEN 8
         WHEN '41' THEN 5
       END,
       TRUE
FROM product_variants v
JOIN sizes s ON s.size_label IN ('36','37','38','39','40','41')
ON CONFLICT (variant_id, size_id)
DO UPDATE SET stock_quantity = EXCLUDED.stock_quantity,
              available = EXCLUDED.available;
