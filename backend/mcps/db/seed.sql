-- =========================================    
-- ========== PROVIDERS ==========
-- =========================================    
INSERT INTO providers (provider_id, name, description, email)
VALUES
    (1, 'Aldo', 'Leading global footwear and accessories brand.', 'contact@aldo.com'),
    (2, 'Clarks', 'Renowned for quality and comfort in shoes.', 'info@clarks.com'),
    (3, 'Zara', 'Fashion-forward retailer with a wide range of shoes and accessories.', 'support@zara.com')
ON CONFLICT (provider_id) DO NOTHING;


-- =========================================    
-- ========== PRODUCTS ==========
-- =========================================    
INSERT INTO products (product_id, sku, category, brand, provider_id)
VALUES
(9, 'MJWEDGE', 'Shoes', 'Aldo', 1),

(10, 'MJPATENT', 'Shoes', 'Aldo',  1),

(11, 'PEEPSTUD','Shoes', 'Clarks', 2),

(12, 'ANKLBOOT','Boot', 'Clarks',2),

(13, 'METSUEDE' ,'Shoes', 'Aldo', 1),

(14, 'PLATSANDL','Sandals', 'Aldo', 1),

(15, 'EMBPEEP','Shoes', 'Clarks', 2),

(16, 'MJWEDGE', 'Shoes', 'Clarks', 2),

(17, 'STUDCLR','Sandals', 'Aldo',1),

(18, 'CLRWEDGE', 'Sandals', 'Zara', 3),

(19, 'COMF3-BEI', 'Sandals', 'Zara', 3),

(20, 'COMF3','Comfort Sandals', 'Aldo', 1),

(21, 'HTBOOT','Boots', 'Zara', 3),

(22, 'RIDING', 'Boots', 'Aldo', 1),

(23, 'RIDING', 'Boots', 'Aldo', 1)
ON CONFLICT (product_id) DO NOTHING;

-- =========================================    
-- ========== PRODUCT VARIANTS ==========
-- =========================================    
INSERT INTO product_variants (variant_id, product_id, variant_sku, name, description, category, color, material, gender, brand, price, image_url, tags_string)
VALUES
(9,9, 'MJWEDGE-BLK', 'MJ Wedge Shoe',
 'Enjoy the perfect blend of height and comfort with this Mary Jane wedge that takes you from office to evening effortlessly. The secure ankle strap ensures stability while the wedge platform provides all-day wearability without compromising on elegance.',
 'Shoes', 'Black', 'Synthetic Leather', 'Women', 'Aldo', 34.50, 'MJWEDGE_black.jpg',
 'black wedge, mary jane style, ankle strap, synthetic leather, aldo, casual wear, dress shoes, platform wedge, comfortable heel, aldo, women''s shoes'),

(10,10, 'MJPATENT', 'Mary Jane Patent Shoe',
 'Step into polished sophistication with this patent Mary Jane that adapts to any dress code. The stable block heel offers confident stride while the classic ankle strap keeps you secure through busy days and special occasions alike.',
 'Shoes', 'Black', 'Synthetic', 'Women', 'Aldo',  39.99, 'MJPATENT_black.jpg',
 'black patent leather, mary jane style, block heel, ankle strap, synthetic leather, aldo, casual wear, dress shoes, formal wear, glossy finish, aldo, women''s shoes, low-heel, medium-heel'),

(11,11, 'PEEPSTUD', 'Studded Peep Toe',
 'Command attention at every special event with these show-stopping studded heels. The peep toe design keeps you comfortable while the bold red hue and metallic stud detailing ensure you stand out, making these the perfect choice for weddings, galas, and celebrations.',
 'Shoes', 'Red','Leather', 'Women', 'Clarks', 89.99, 'PEEPSTUD.jpg',
 'red peep toe, studded heels, clarks, stiletto heel, leather, formal wear, special occasion, dress shoes, statement heels, high-heel, aldo, women''s shoes'),

(12,12, 'ANKLBOOT', 'Ankle Boot',
 'Elevate your evening wardrobe with these sleek ankle boots that deliver runway-ready height without sacrificing stability. The platform base balances the dramatic heel while the side zipper ensures easy on-and-off, making these your go-to choice for formal events and nights out.',
 'Boot', 'Black','Synthetic Leather', 'Women', 'Clarks', 119.00, 'ANKLBOOT.jpg',
 'black ankle boot, high heel boot, synthetic leather, formal wear, stiletto heel, platform boot, side zipper, dress boots, clarks, women''s boots'),

(13,13, 'METSUEDE', 'Metallic Heel Shoe',
 'Step confidently into any event with these dramatic platform heels that maximize height while maintaining comfort. The elevated platform front reduces the pitch of the heel, letting you stand tall through extended wear at formal gatherings and special occasions.',
 'Shoes', 'Black', 'Suede', 'Women', 'Aldo', 99.00, 'METSUEDE.jpg',
 'black platform heels, synthetic suede, stiletto heel, platform pumps, formal wear, dress shoes, high heel, slip-on, aldo, women''s platform shoes'),

(14,14, 'PLATSANDL', 'Platform Shandal',
 'Make a vibrant statement at your next celebration with these eye-catching platform sandals. The supportive strappy design keeps your feet secure while the platform base provides added comfort for dancing and mingling through weddings, parties, and special events.',
 'Sandals', 'Orange','Synthetic Leather', 'Women', 'Clarks', 79.50, 'PLATSANDL.jpg',
 'orange platform sandal, strappy heels, synthetic leather, stiletto heel, dress shoes, special occasion, party heels, high heel sandal, clarks, women''s platform sandals'),

(15,15, 'EMBPEEP', 'Embellished Peep Toe',
 'Turn heads at every celebration with these stunning peep toe heels featuring elegant toe embellishments. The open-toe design keeps you comfortable while the bold red color and decorative studs ensure you shine at weddings, parties, and all your special moments.',
 'Shoes', 'Red','Synthetic', 'Women', 'Clarks', 94.00, 'EMBPEEP.jpg',
 'red peep toe, embellished heels, synthetic leather, stiletto heel, high-heel, special occasion, dress shoes, party heels, studded toe, clarks, women''s heels'),

(16,16, 'MJWEDGE-BRN', 'MJ Wedge Shoe (Brown)',
 'Enjoy the perfect blend of height and comfort with this Mary Jane wedge that takes you from office to evening effortlessly. The secure ankle strap ensures stability while the wedge platform provides all-day wearability without compromising on elegance.',
 'Shoes', 'Brown','Synthetic Leather', 'Women', 'Aldo',  34.50, 'MJWEDGE_brown.jpg',
 'brown wedge, mary jane style, ankle strap, synthetic leather, aldo, casual wear, dress shoes, platform wedge, low-heel, comfortable heel, aldo, women''s shoes'),

(17,17, 'STUDCLR', 'Stud Clear Shoe',
 'Stand out at your next event with these modern sandals featuring transparent straps and eye-catching stud details. The unique sculptural heel adds contemporary flair while the secure strap design keeps you comfortable through parties, cocktail events, and dressy occasions.',
 'Sandals', 'Black','Synthetic', 'Women', 'Zara',39.90, 'STUDCLR-BLK.jpg',
 'black studded sandal, clear strap heels, transparent straps, synthetic leather, special occasion, dress shoes, party heels, medium-heels, sculptural heel, zara, women''s sandals'),

(18,18, 'CLRWEDGE', 'Clear Wedge Gold',
 'Combine elegance with comfort in these stunning wedge sandals featuring delicate transparent straps and luxe gold accents. The wedge heel provides stability for dancing and socializing through parties and special events while the barely-there design keeps your look light and sophisticated.',
 'Sandals', 'Gold','Synthetic', 'Women', 'Zara', 42.00, 'CLRWEDGE-GLD.jpg',
 'gold wedge sandal, clear straps, transparent heels, synthetic leather, special occasion, dress shoes, party heels, low-heel, minimalist design, zara, women''s wedge sandals'),

(19,19, 'COMF3-BEI', 'Comfort 3 Shoe Beige',
 'Discover all-day comfort with these practical sandals designed for extended wear. The adjustable velcro straps ensure a personalized fit while the cushioned footbed supports your feet through long walks, errands, and everyday activities without compromising on style.',
 'Sandals', 'Beige','Synthetic', 'Women', 'Aldo', 59.00, 'COMF3-BEI.jpg',
 'comfort sandals, walking shoes, adjustable straps, beige, synthetic leather, casual wear, velcro straps, cushioned footbed, everyday comfort, aldo, women''s comfort shoes'),

(20,20, 'COMF3-BLK', 'Comfort 3 Shoe Black',
 'Discover all-day comfort with these practical sandals designed for extended wear. The adjustable velcro straps ensure a personalized fit while the cushioned footbed supports your feet through long walks, errands, and everyday activities without compromising on style.',
 'Sandals', 'Black','Synthetic', 'Women', 'Aldo',59.00, 'COMF3-BLK.jpg',
 'comfort sandals, walking shoes, adjustable straps, synthetic leather, casual wear, black, velcro straps, cushioned footbed, everyday comfort, aldo, women''s comfort shoes'),

(21,21 ,'HTBOOT', 'High Top Boot',
 'Elevate your everyday style with these versatile knee-high boots that transition seamlessly from casual outings to dressier occasions. The sleek silhouette flatters your legs while the side zipper ensures easy wear, making these your go-to boots for creating polished looks all season long.',
 'Boots', 'Brown','Synthetic Leather', 'Women', 'Zara', 129.00, 'HTBOOT-BRN.jpg',
 'brown knee-high boot, stiletto heel, synthetic leather, dress boots, casual wear, high top boot, side zipper, fashion boots, zara, women''s boots'),

(22,22, 'RIDING-BLK', 'Riding Boot Black',
 'Step into effortless everyday style with these classic riding boots that deliver all-day comfort without sacrificing sophistication. The low heel and cushioned footbed support your feet through busy days while the timeless silhouette pairs perfectly with jeans, leggings, or dresses for versatile wear.',
 'Boots', 'Black','Synthetic Leather', 'Women', 'Aldo',119.00, 'RIDING-BLK.jpg',
 'black riding boot, low heel boot, synthetic leather, casual wear, everyday comfort, knee-high boot, side zipper, equestrian style, aldo, women''s boots'),

(23,23, 'RIDING-COG', 'Riding Boot Cognac',
 'Step into effortless everyday style with these classic riding boots that deliver all-day comfort without sacrificing sophistication. The low heel and cushioned footbed support your feet through busy days while the timeless silhouette pairs perfectly with jeans, leggings, or dresses for versatile wear.',
 'Boots', 'Cognac','Synthetic Leather', 'Women', 'Aldo', 119.00, 'RIDING-COG.jpg',
 'cognac riding boot, granate riding boot, granate, low heel boot, synthetic leather, casual wear, everyday comfort, knee-high boot, side zipper, equestrian style, aldo, women''s boots')
ON CONFLICT (variant_id) DO NOTHING;

-- =========================================    
-- ========== SIZES ==========
-- =========================================    
INSERT INTO sizes (size_label)
VALUES ('36'),('37'),('38'),('39'),('40'),('41')
ON CONFLICT (size_label) DO NOTHING;


-- =========================================    
-- ========== VARIANT SIZE STOCK MATRIX ==========
-- =========================================    
INSERT INTO variant_sizes (variant_id, size_id, stock_quantity, available)
SELECT v.variant_id, s.size_id,
       CASE s.size_label
         WHEN '36' THEN 2
         WHEN '37' THEN 3
         WHEN '38' THEN 4
         WHEN '39' THEN 3
         WHEN '40' THEN 2
         WHEN '41' THEN 1
       END AS stock_quantity,
       TRUE AS available
FROM product_variants v
CROSS JOIN sizes s
WHERE s.size_label IN ('36','37','38','39','40','41')
ON CONFLICT (variant_id, size_id)
DO UPDATE SET 
    stock_quantity = EXCLUDED.stock_quantity,
    available = EXCLUDED.available;


-- =========================================    
-- ========== CITIES ==========
-- =========================================    
INSERT INTO cities (city) VALUES
('New York'), ('Los Angeles'), ('Chicago'), ('Houston'), ('Phoenix'),
('Philadelphia'), ('San Antonio'), ('San Diego'), ('Dallas'), ('San Jose'),
('Austin'), ('Jacksonville'), ('Fort Worth'), ('Columbus'), ('Charlotte'),
('San Francisco'), ('Indianapolis'), ('Seattle'), ('Denver'), ('Washington'),
('Boston'), ('El Paso'), ('Portland'), ('Detroit'), ('Oklahoma City'),
('Las Vegas'), ('Memphis');



-- =========================================    
-- ========== PAYMENT METHODS ==========
-- =========================================    
INSERT INTO payment_methods (method_name) VALUES
('Credit Card'),
('Debit Card'),
('PayPal'),
('Apple Pay'),
('Google Pay'),
('Gift Card'),
('Cash');



-- =========================================
-- COMPREHENSIVE SALES DATA (Last 6 Months)
-- ~1000 sales from May 2024 to November 2024
-- =========================================
------------------------------------------------------------
-- GENERATE ~1000 SALES WITH REALISTIC MONTHLY DISTRIBUTION
------------------------------------------------------------

TRUNCATE sales RESTART IDENTITY CASCADE;
TRUNCATE sale_line_item RESTART IDENTITY;

DO $$
DECLARE
    month_list RECORD;
    target_count INTEGER;
    daily_sales INTEGER;
    sale_dt DATE;
    weekday INTEGER;
    weekend_sales INTEGER;
    weekday_sales INTEGER;
    day_counter INTEGER;
BEGIN
    FOR month_list IN 
        SELECT * FROM (VALUES
            (2025, 5, 140),
            (2025, 6, 150),
            (2025, 7, 180),
            (2025, 8, 170),
            (2025, 9, 160),
            (2025,10, 170),
            (2025,11, 200)
        ) AS m (yr, mon, cnt)
    LOOP
        -- Iterate each day in the month
        FOR day_counter IN 1..EXTRACT(DAY FROM make_date(month_list.yr, month_list.mon, 1)
                                        + INTERVAL '1 month' - INTERVAL '1 day') LOOP
            
            sale_dt := make_date(month_list.yr, month_list.mon, day_counter);
            weekday := EXTRACT(DOW FROM sale_dt);

            -- Weekend boost: Sat(6) & Sun(0)
            IF weekday = 6 OR weekday = 0 THEN
                weekend_sales := 7; -- 6–8 typical
                daily_sales := 6 + FLOOR(RANDOM() * 2);
            ELSE
                daily_sales := 4 + FLOOR(RANDOM() * 2);  -- 4–5 weekday
            END IF;

            -- Insert daily sales
            FOR i IN 1..daily_sales LOOP
                INSERT INTO sales (customer_city, payment_method, sale_date)
                VALUES (
                    (SELECT city FROM cities ORDER BY RANDOM() LIMIT 1),
                    (SELECT method_name FROM payment_methods ORDER BY RANDOM() LIMIT 1),
                    sale_dt::timestamp
                );
            END LOOP;

        END LOOP;
    END LOOP;
END $$;

------------------------------------------------------------
-- SALE LINE ITEMS USING REAL VARIANT PRICES
------------------------------------------------------------

DO $$
DECLARE
    sale_record RECORD;
    num_items INTEGER;
    variant_id_choice INTEGER;
    quantity_choice INTEGER;
    base_price NUMERIC;
    sale_price NUMERIC;
    discount_factor NUMERIC;

    -- Weight popular variants heavy
    popular_variants INTEGER[] := ARRAY[
        9,9,9,  -- best sellers
        11,11,11,
        14,14, 
        16,16,
        23,23
    ];
BEGIN
    FOR sale_record IN SELECT sale_id, sale_date FROM sales LOOP

        -- 80% buy 1 item, 15% buy 2, 5% buy 3
        num_items := CASE
            WHEN RANDOM() < 0.80 THEN 1
            WHEN RANDOM() < 0.95 THEN 2
            ELSE 3
        END;

        -- Black Friday discount mid-late November
        discount_factor := CASE
            WHEN EXTRACT(MONTH FROM sale_record.sale_date) = 11
                AND EXTRACT(DAY FROM sale_record.sale_date) >= 15
            THEN 0.80 + (RANDOM() * 0.10)
            ELSE 1.00
        END;

        FOR j IN 1..num_items LOOP

            -- 70% popular items, 30% random
            IF RANDOM() < 0.70 THEN
                variant_id_choice := popular_variants[
                    1 + FLOOR(RANDOM() * array_length(popular_variants, 1))
                ];
            ELSE
                SELECT variant_id INTO variant_id_choice
                FROM product_variants ORDER BY RANDOM() LIMIT 1;
            END IF;

            -- Quantity distribution
            quantity_choice := CASE
                WHEN RANDOM() < 0.90 THEN 1
                WHEN RANDOM() < 0.98 THEN 2
                ELSE 3
            END;

            -- Real price from DB
            SELECT price INTO base_price
            FROM product_variants
            WHERE variant_id = variant_id_choice;

            sale_price := ROUND(base_price * discount_factor, 2);

            INSERT INTO sale_line_item (sale_id, variant_id, quantity, unit_price)
            VALUES (sale_record.sale_id, variant_id_choice, quantity_choice, sale_price);

        END LOOP;

    END LOOP;
END $$;



--- PROVIDERS
SELECT setval(
    'providers_provider_id_seq',
    COALESCE((SELECT MAX(provider_id) FROM providers), 0) + 1,
    true
);

-- PRODUCTS
SELECT setval(
    'products_product_id_seq',
    COALESCE((SELECT MAX(product_id) FROM products), 0) + 1,
    true
);

-- PRODUCT VARIANTS
SELECT setval(
    'product_variants_variant_id_seq',
    COALESCE((SELECT MAX(variant_id) FROM product_variants), 0) + 1,
    true
);

-- SIZES
SELECT setval(
    'sizes_size_id_seq',
    COALESCE((SELECT MAX(size_id) FROM sizes), 0) + 1,
    true
);

-- TAGS
SELECT setval(
    'tags_tag_id_seq',
    COALESCE((SELECT MAX(tag_id) FROM tags), 0) + 1,
    true
);

-- VARIANT METADATA
SELECT setval(
    'variant_metadata_metadata_id_seq',
    COALESCE((SELECT MAX(metadata_id) FROM variant_metadata), 0) + 1,
    true
);

-- SALES
SELECT setval(
    'sales_sale_id_seq',
    COALESCE((SELECT MAX(sale_id) FROM sales), 0) + 1,
    true
);

-- SALE LINE ITEMS
SELECT setval(
    'sale_line_item_line_item_id_seq',
    COALESCE((SELECT MAX(line_item_id) FROM sale_line_item), 0) + 1,
    true
);

-- CITIES
SELECT setval(
    'cities_id_seq',
    COALESCE((SELECT MAX(id) FROM cities), 0) + 1,
    true
);

-- PAYMENT METHODS
SELECT setval(
    'payment_methods_method_id_seq',
    COALESCE((SELECT MAX(method_id) FROM payment_methods), 0) + 1,
    true
);

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


-- SELECT TO_CHAR(sale_date, 'YYYY-MM') as month,COUNT(*) as sales_count,SUM(sli.quantity * sli.unit_price) as total_revenue
 -- FROM sales s
 -- JOIN sale_line_item sli ON s.sale_id = sli.sale_id
--  GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
 -- ORDER BY month;