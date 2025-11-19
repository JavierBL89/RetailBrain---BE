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




-- =========================================
-- COMPREHENSIVE SALES DATA (Last 6 Months)
-- ~1000 sales from May 2024 to November 2024
-- =========================================
DO $$
DECLARE
    sale_counter INTEGER := 1;
    line_counter INTEGER := 1;
    sale_timestamp TIMESTAMP;
    days_in_month INTEGER;
    sales_per_day INTEGER;
    i INTEGER;
    j INTEGER;
    variant_choice INTEGER;
    quantity_choice INTEGER;
    sale_hour INTEGER;
    customer_names TEXT[] := ARRAY[
        'Emma Johnson', 'Michael Chen', 'Sarah Williams', 'James Martinez', 'Olivia Brown',
        'Noah Davis', 'Ava Garcia', 'Liam Rodriguez', 'Isabella Wilson', 'Sophia Moore',
        'Mason Taylor', 'Charlotte Anderson', 'Ethan Thomas', 'Amelia Jackson', 'Lucas White',
        'Mia Harris', 'Harper Martin', 'Alexander Thompson', 'Evelyn Garcia', 'Benjamin Martinez',
        'Abigail Rodriguez', 'Daniel Hernandez', 'Emily Lopez', 'Henry Gonzalez', 'Elizabeth Wilson'
    ];
    locations TEXT[] := ARRAY[
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
        'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus',
        'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington DC',
        'Boston', 'Nashville', 'Portland', 'Las Vegas', 'Detroit', 'Miami', 'Atlanta'
    ];
    payment_methods TEXT[] := ARRAY['Credit Card', 'Debit Card', 'PayPal', 'Cash', 'Apple Pay'];
BEGIN
    -- MAY 2024: 140 sales
    FOR i IN 1..31 LOOP
        sales_per_day := CASE 
            WHEN i % 7 IN (0, 6) THEN 6  -- Weekends
            ELSE 4  -- Weekdays
        END;
        
        FOR j IN 1..sales_per_day LOOP
            sale_hour := 9 + ((j - 1) % 12);
            sale_timestamp := ('2024-05-' || LPAD(i::TEXT, 2, '0') || ' ' || 
                           LPAD(sale_hour::TEXT, 2, '0') || ':' ||
                           LPAD((RANDOM() * 59)::INTEGER::TEXT, 2, '0') || ':00')::TIMESTAMP;
            
            INSERT INTO sales (customer_name, location, payment_method, sale_date)
            VALUES (
                customer_names[1 + (RANDOM() * (array_length(customer_names, 1) - 1))::INTEGER],
                locations[1 + (RANDOM() * (array_length(locations, 1) - 1))::INTEGER],
                payment_methods[1 + (RANDOM() * (array_length(payment_methods, 1) - 1))::INTEGER],
                sale_timestamp
            );
            
            sale_counter := sale_counter + 1;
        END LOOP;
    END LOOP;
    
    -- JUNE 2024: 150 sales
    FOR i IN 1..30 LOOP
        sales_per_day := CASE 
            WHEN i % 7 IN (0, 6) THEN 7
            ELSE 4
        END;
        
        FOR j IN 1..sales_per_day LOOP
            sale_hour := 9 + ((j - 1) % 12);
            sale_timestamp := ('2024-06-' || LPAD(i::TEXT, 2, '0') || ' ' || 
                           LPAD(sale_hour::TEXT, 2, '0') || ':' ||
                           LPAD((RANDOM() * 59)::INTEGER::TEXT, 2, '0') || ':00')::TIMESTAMP;
            
            INSERT INTO sales (customer_name, location, payment_method, sale_date)
            VALUES (
                customer_names[1 + (RANDOM() * (array_length(customer_names, 1) - 1))::INTEGER],
                locations[1 + (RANDOM() * (array_length(locations, 1) - 1))::INTEGER],
                payment_methods[1 + (RANDOM() * (array_length(payment_methods, 1) - 1))::INTEGER],
                sale_timestamp
            );
        END LOOP;
    END LOOP;
    
    -- JULY 2024: 180 sales (summer peak)
    FOR i IN 1..31 LOOP
        sales_per_day := CASE 
            WHEN i % 7 IN (0, 6) THEN 8
            WHEN i = 4 THEN 12  -- July 4th spike
            ELSE 5
        END;
        
        FOR j IN 1..sales_per_day LOOP
            sale_hour := 9 + ((j - 1) % 12);
            sale_timestamp := ('2024-07-' || LPAD(i::TEXT, 2, '0') || ' ' || 
                           LPAD(sale_hour::TEXT, 2, '0') || ':' ||
                           LPAD((RANDOM() * 59)::INTEGER::TEXT, 2, '0') || ':00')::TIMESTAMP;
            
            INSERT INTO sales (customer_name, location, payment_method, sale_date)
            VALUES (
                customer_names[1 + (RANDOM() * (array_length(customer_names, 1) - 1))::INTEGER],
                locations[1 + (RANDOM() * (array_length(locations, 1) - 1))::INTEGER],
                payment_methods[1 + (RANDOM() * (array_length(payment_methods, 1) - 1))::INTEGER],
                sale_timestamp
            );
        END LOOP;
    END LOOP;
    
    -- AUGUST 2024: 170 sales (back to school)
    FOR i IN 1..31 LOOP
        sales_per_day := CASE 
            WHEN i BETWEEN 15 AND 25 THEN 7  -- Back to school rush
            WHEN i % 7 IN (0, 6) THEN 7
            ELSE 4
        END;
        
        FOR j IN 1..sales_per_day LOOP
            sale_hour := 9 + ((j - 1) % 12);
            sale_timestamp := ('2024-08-' || LPAD(i::TEXT, 2, '0') || ' ' || 
                           LPAD(sale_hour::TEXT, 2, '0') || ':' ||
                           LPAD((RANDOM() * 59)::INTEGER::TEXT, 2, '0') || ':00')::TIMESTAMP;
            
            INSERT INTO sales (customer_name, location, payment_method, sale_date)
            VALUES (
                customer_names[1 + (RANDOM() * (array_length(customer_names, 1) - 1))::INTEGER],
                locations[1 + (RANDOM() * (array_length(locations, 1) - 1))::INTEGER],
                payment_methods[1 + (RANDOM() * (array_length(payment_methods, 1) - 1))::INTEGER],
                sale_timestamp
            );
        END LOOP;
    END LOOP;
    
    -- SEPTEMBER 2024: 160 sales (fall season)
    FOR i IN 1..30 LOOP
        sales_per_day := CASE 
            WHEN i % 7 IN (0, 6) THEN 7
            ELSE 4
        END;
        
        FOR j IN 1..sales_per_day LOOP
            sale_hour := 9 + ((j - 1) % 12);
            sale_timestamp := ('2024-09-' || LPAD(i::TEXT, 2, '0') || ' ' || 
                           LPAD(sale_hour::TEXT, 2, '0') || ':' ||
                           LPAD((RANDOM() * 59)::INTEGER::TEXT, 2, '0') || ':00')::TIMESTAMP;
            
            INSERT INTO sales (customer_name, location, payment_method, sale_date)
            VALUES (
                customer_names[1 + (RANDOM() * (array_length(customer_names, 1) - 1))::INTEGER],
                locations[1 + (RANDOM() * (array_length(locations, 1) - 1))::INTEGER],
                payment_methods[1 + (RANDOM() * (array_length(payment_methods, 1) - 1))::INTEGER],
                sale_timestamp
            );
        END LOOP;
    END LOOP;
    
    -- OCTOBER 2024: 170 sales
    FOR i IN 1..31 LOOP
        sales_per_day := CASE 
            WHEN i % 7 IN (0, 6) THEN 7
            WHEN i = 31 THEN 10  -- Halloween spike
            ELSE 4
        END;
        
        FOR j IN 1..sales_per_day LOOP
            sale_hour := 9 + ((j - 1) % 12);
            sale_timestamp := ('2024-10-' || LPAD(i::TEXT, 2, '0') || ' ' || 
                           LPAD(sale_hour::TEXT, 2, '0') || ':' ||
                           LPAD((RANDOM() * 59)::INTEGER::TEXT, 2, '0') || ':00')::TIMESTAMP;
            
            INSERT INTO sales (customer_name, location, payment_method, sale_date)
            VALUES (
                customer_names[1 + (RANDOM() * (array_length(customer_names, 1) - 1))::INTEGER],
                locations[1 + (RANDOM() * (array_length(locations, 1) - 1))::INTEGER],
                payment_methods[1 + (RANDOM() * (array_length(payment_methods, 1) - 1))::INTEGER],
                sale_timestamp
            );
        END LOOP;
    END LOOP;
    
    -- NOVEMBER 2024: 200 sales (Black Friday)
    FOR i IN 1..18 LOOP
        sales_per_day := CASE 
            WHEN i IN (28, 29) THEN 20  -- Black Friday weekend (simulated)
            WHEN i % 7 IN (0, 6) THEN 8
            ELSE 5
        END;
        
        -- Adjust for actual Black Friday in 2024 (Nov 29)
        IF i >= 15 THEN
            sales_per_day := sales_per_day + 5;  -- Holiday shopping increase
        END IF;
        
        FOR j IN 1..sales_per_day LOOP
            sale_hour := 9 + ((j - 1) % 12);
            sale_timestamp := ('2024-11-' || LPAD(i::TEXT, 2, '0') || ' ' || 
                           LPAD(sale_hour::TEXT, 2, '0') || ':' ||
                           LPAD((RANDOM() * 59)::INTEGER::TEXT, 2, '0') || ':00')::TIMESTAMP;
            
            INSERT INTO sales (customer_name, location, payment_method, sale_date)
            VALUES (
                customer_names[1 + (RANDOM() * (array_length(customer_names, 1) - 1))::INTEGER],
                locations[1 + (RANDOM() * (array_length(locations, 1) - 1))::INTEGER],
                payment_methods[1 + (RANDOM() * (array_length(payment_methods, 1) - 1))::INTEGER],
                sale_timestamp
            );
        END LOOP;
    END LOOP;
END $$;

-- =========================================
-- SALE LINE ITEMS WITH REALISTIC PATTERNS
-- =========================================
DO $$
DECLARE
    sale_record RECORD;
    num_items INTEGER;
    i INTEGER;
    variant_id_choice INTEGER;
    quantity_choice INTEGER;
    base_price NUMERIC(10,2);
    sale_price NUMERIC(10,2);
    discount_factor NUMERIC(3,2);
    
    -- Variant pricing
    variant_prices NUMERIC[] := ARRAY[34.50, 34.50, 39.99, 89.99, 119.00, 99.00, 79.50, 94.00, 39.90, 42.00, 59.00, 59.00, 129.00, 119.00, 119.00];
    
    -- Weight distribution for popular items (variants 1, 3, 7, 11, 14 are popular)
    popular_variants INTEGER[] := ARRAY[1, 1, 1, 3, 3, 3, 7, 7, 11, 11, 11, 14, 14];
BEGIN
    FOR sale_record IN SELECT sale_id, sale_date FROM sales ORDER BY sale_id LOOP
        -- Determine number of items in this sale (80% single item, 15% two items, 5% three items)
        num_items := CASE 
            WHEN RANDOM() < 0.80 THEN 1
            WHEN RANDOM() < 0.95 THEN 2
            ELSE 3
        END;
        
        -- Black Friday discounts (November sales get 10-20% off)
        discount_factor := CASE 
            WHEN EXTRACT(MONTH FROM sale_record.sale_date) = 11 AND EXTRACT(DAY FROM sale_record.sale_date) >= 15 
            THEN 0.80 + (RANDOM() * 0.10)::NUMERIC  -- 10-20% off
            ELSE 1.00
        END;
        
        FOR i IN 1..num_items LOOP
            -- 70% chance to pick from popular items, 30% random
            IF RANDOM() < 0.70 THEN
                variant_id_choice := popular_variants[1 + (RANDOM() * (array_length(popular_variants, 1) - 1))::INTEGER];
            ELSE
                variant_id_choice := 1 + (RANDOM() * 14)::INTEGER;
            END IF;
            
            -- Quantity (90% buy 1, 8% buy 2, 2% buy 3+)
            quantity_choice := CASE 
                WHEN RANDOM() < 0.90 THEN 1
                WHEN RANDOM() < 0.98 THEN 2
                ELSE 3
            END;
            
            -- Get base price and apply discount
            base_price := variant_prices[variant_id_choice];
            sale_price := ROUND(base_price * discount_factor, 2);
            
            INSERT INTO sale_line_item (sale_id, variant_id, quantity, unit_price)
            VALUES (sale_record.sale_id, variant_id_choice, quantity_choice, sale_price);
        END LOOP;
    END LOOP;
END $$;

-- =========================================
-- VERIFICATION QUERIES
-- =========================================
-- Uncomment these to verify your data after loading

-- Total sales count
-- SELECT COUNT(*) as total_sales FROM sales;

-- Sales by month
-- SELECT 
--     TO_CHAR(sale_date, 'YYYY-MM') as month,
--     COUNT(*) as sales_count,
--     SUM(sli.quantity * sli.unit_price) as total_revenue
-- FROM sales s
-- JOIN sale_line_item sli ON s.sale_id = sli.sale_id
-- GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
-- ORDER BY month;

-- Top selling products
-- SELECT 
--     p.name,
--     v.color,
--     SUM(sli.quantity) as total_sold,
--     SUM(sli.quantity * sli.unit_price) as revenue
-- FROM sale_line_item sli
-- JOIN product_variants v ON sli.variant_id = v.variant_id
-- JOIN products p ON v.product_id = p.product_id
-- GROUP BY p.name, v.color
-- ORDER BY total_sold DESC
-- LIMIT 10;

-- Average order value
-- SELECT 
--     ROUND(AVG(order_total), 2) as avg_order_value
-- FROM (
--     SELECT s.sale_id, SUM(sli.quantity * sli.unit_price) as order_total
--     FROM sales s
--     JOIN sale_line_item sli ON s.sale_id = sli.sale_id
--     GROUP BY s.sale_id
-- ) subquery;


SELECT TO_CHAR(sale_date, 'YYYY-MM') as month,COUNT(*) as sales_count,SUM(sli.quantity * sli.unit_price) as total_revenue
 FROM sales s
 JOIN sale_line_item sli ON s.sale_id = sli.sale_id
 GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
 ORDER BY month;