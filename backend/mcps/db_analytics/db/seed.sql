-- =========================================    
-- ========== PRODUCTS ==========
-- =========================================    
INSERT INTO products (product_id, sku, name, description, category, material, gender, brand, tags_string)
VALUES
(9, 'MJWEDGE', 'MJ Wedge Shoe', 'Auto-generated product', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'wedge,auto'),
(10, 'MJPATENT', 'Mary Jane Patent Shoe', 'Auto-generated product', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'mary jane,auto'),
(11, 'PEEPSTUD', 'Studded Peep Toe', 'Auto-generated product', 'Shoes', 'Leather', 'Women', 'Unknown', 'peep toe,stud,auto'),
(12, 'ANKLBOOT', 'Ankle Boot', 'Auto-generated product', 'Shoes', 'Leather', 'Women', 'Unknown', 'boot,ankle,auto'),
(13, 'METSUEDE', 'Metallic Heel Shoe', 'Auto-generated product', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'heel,metallic,auto'),
(14, 'PLATSANDL', 'Platform Sandal', 'Auto-generated product', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'sandal,platform,auto'),
(15, 'EMBPEEP', 'Embellished Peep Toe', 'Auto-generated product', 'Shoes', 'Leather', 'Women', 'Unknown', 'peep toe,embellished,auto'),
(16, 'MJWEDGE-BRN', 'MJ Wedge Shoe (Brown)', 'Auto product', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'wedge,auto'),
(17, 'STUDCLR', 'Stud Clear Shoe', 'Auto-generated product', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'stud,clear,auto'),
(18, 'CLRWEDGE', 'Clear Wedge Gold', 'Auto-generated product', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'wedge,clear,gold,auto'),
(19, 'COMF3-BEI', 'Comfort 3 Shoe Beige', 'Comfort shoes', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'comfort,auto'),
(20, 'COMF3-BLK', 'Comfort 3 Shoe Black', 'Comfort shoes', 'Shoes', 'Synthetic', 'Women', 'Unknown', 'comfort,auto'),
(21, 'HTBOOT', 'High Top Boot', 'Auto-generated product', 'Shoes', 'Leather', 'Women', 'Unknown', 'boot,high,auto'),
(22, 'RIDING-BLK', 'Riding Boot Black', 'Auto-generated product', 'Shoes', 'Leather', 'Women', 'Unknown', 'riding,boot,auto'),
(23, 'RIDING-COG', 'Riding Boot Cognac', 'Auto-generated product', 'Shoes', 'Leather', 'Women', 'Unknown', 'riding,boot,auto')
ON CONFLICT (product_id) DO NOTHING;

-- =========================================    
-- ========== SIZES ==========
-- =========================================    
INSERT INTO sizes (size_label)
VALUES ('36'),('37'),('38'),('39'),('40'),('41')
ON CONFLICT (size_label) DO NOTHING;

-- =========================================    
-- ========== PRODUCT VARIANTS ==========
-- =========================================    
INSERT INTO product_variants (product_id, variant_sku, color, price, image_url) 
VALUES
(9,  'MJWEDGE-BLK', 'Black', 34.50, 'MJWEDGE_black.jpg'),
(16, 'MJWEDGE-BRN', 'Brown', 34.50, 'MJWEDGE_brown.jpg'),
(10, 'MJPATENT-BLK', 'Black', 39.99, 'MJPATENT_black.jpg'),
(11, 'PEEPSTUD-RED', 'Red/Brown/Gold', 89.99, 'PEEPSTUD.jpg'),
(12, 'ANKLBOOT-BLK', 'Black', 119.00, 'ANKLBOOT.jpg'),
(13, 'METSUEDE-BLK', 'Black', 99.00, 'METSUEDE.jpg'),
(14, 'PLATSANDL-ORG', 'Orange', 79.50, 'PLATSANDL.jpg'),
(15, 'EMBPEEP-RED', 'Red', 94.00, 'EMBPEEP.jpg'),
(17, 'STUDCLR-BLK', 'Black', 39.90, 'STUDCLR-BLK.jpg'),
(18, 'CLRWEDGE-GLD', 'Gold/Clear', 42.00, 'CLRWEDGE-GLD.jpg'),
(19, 'COMF3-BEI', 'Beige', 59.00, 'COMF3-BEI.jpg'),
(20, 'COMF3-BLK', 'Black', 59.00, 'COMF3-BLK.jpg'),
(21, 'HTBOOT-BRN', 'Brown', 129.00, 'HTBOOT-BRN.jpg'),
(22, 'RIDING-BLK', 'Black', 119.00, 'RIDING-BLK.jpg'),
(23, 'RIDING-COG', 'Cognac', 119.00, 'RIDING-COG.jpg');

-- =========================================    
-- ========== VARIANT SIZE STOCK MATRIX ==========
-- =========================================    
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
CROSS JOIN sizes s
WHERE s.size_label IN ('36','37','38','39','40','41')
ON CONFLICT (variant_id, size_id)
DO UPDATE SET stock_quantity = EXCLUDED.stock_quantity,
              available = EXCLUDED.available;