INSERT INTO products (sku, name, description, category, material, gender, brand)
VALUES
('CLR-HEEL-SANDAL', 'Clear Heel Dress Sandal', 'Strappy sandal with iron embellishments.', 'Sandal', 'Synthetic / TPU', 'Women', 'Unknown'),
('STC-HEEL-SANDAL', 'Sofi Heel Dress Sandal', 'Strappy sandal with transparent heel.', 'Sandal', 'Synthetic / TPU', 'Women', 'Unknown'),
('VELCRO-COMFORT-Brown', 'Comfort Velcro Sandal', 'Comfort velcro sandal with adjustable velcro straps.', 'Sandal', 'Leather / Synthetic', 'Women', 'Unknown'),
('VELCRO-COMFORT-Black', 'Comfort Sandal', 'Comfort velcro sandal with adjustable velcro straps.', 'Sandal', 'Leather / Synthetic', 'Women', 'Unknown'),
('KNEE-HIGH-STILETTO', 'High Heel Knee Boot', 'Tall knee-high stiletto boot with platform.', 'Boot', 'Leather / Synthetic', 'Women', 'Unknown'),
('RIDING-BOOT-FLAT', 'Flat Riding Boot', 'Tall flat riding boot, everyday comfort.', 'Boot', 'Leather / Synthetic', 'Women', 'Unknown'),
('RIDING-BOOT-BLOCK', 'Block Heel Riding Boot', 'Knee-high boot with block heel.', 'Boot', 'Leather / Synthetic', 'Women', 'Unknown');


INSERT INTO product_variants (product_id, variant_sku, color, price, image_url)
VALUES

(17, 'STUDCLR-BLK', 'Black', 39.90, 'STUDCLR-BLK.jpg'),


(18, 'CLRWEDGE-GLD', 'Gold/Clear', 42.00, 'CLRWEDGE-GLD.jpg'),

(19, 'COMF3-BEI', 'Beige', 59.00, 'COMF3-BEI.jpg'),


(20, 'COMF3-BLK', 'Black', 59.00, 'COMF3-BLK.jpg'),


(21, 'HTBOOT-BRN', 'Brown', 129.00, 'HTBOOT-BRN.jpg'),


(22, 'RIDING-BLK', 'Black', 119.00, 'RIDING-BLK.jpg'),


(23, 'RIDING-COG', 'Cognac', 119.00, 'RIDING-COG.jpg');



### re-apply stock / sizes automatically

INSERT INTO variant_sizes (variant_id, size_id, stock_quantity, available)
SELECT v.variant_id,
       s.size_id,
       CASE s.size_label
         WHEN '36' THEN 5
         WHEN '37' THEN 8
         WHEN '38' THEN 5
         WHEN '39' THEN 5
         WHEN '40' THEN 8
         WHEN '41' THEN 5
       END AS stock_quantity,
       TRUE
FROM product_variants v
JOIN sizes s ON s.size_label IN ('36','37','38','39','40','41')
WHERE v.variant_sku IN (
  'STUDCLR-BLK',
  'CLRWEDGE-GLD',
  'COMF3-BEI',
  'COMF3-BLK',
  'HTBOOT-BRN',
  'RIDING-BLK',
  'RIDING-COG'
)
ON CONFLICT (variant_id, size_id)
DO UPDATE SET stock_quantity = EXCLUDED.stock_quantity,
              available      = EXCLUDED.available;
