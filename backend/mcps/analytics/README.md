# RetailBrain Database Documentation

## Products Database Overview

### Schema Summary
- **Products**: 15 women's shoe products
- **Product Variants**: 15 color variants (one per product)
- **Sizes**: 6 size options (36-41)
- **Variant-Size Matrix**: 90 combinations (15 variants × 6 sizes)
- **Sales**: ~1,065 transactions over 6 months
- **Sale Line Items**: ~1,200-1,500 items sold

---

## 🗂️ Database Structure

### Core Tables

#### 1. **products**
Main product catalog
- `product_id` - Primary key
- `sku` - Stock keeping unit
- `name` - Product name
- `description` - Product description
- `category` - Product category (e.g., "Shoes")
- `material` - Material type (Leather, Synthetic)
- `gender` - Target gender
- `brand` - Brand name
- `tags_string` - Comma-separated tags

#### 2. **product_variants**
Product variations (colors, styles)
- `variant_id` - Primary key (auto-generated)
- `product_id` - Foreign key to products
- `variant_sku` - Unique variant SKU
- `color` - Color/style name
- `price` - Variant price
- `image_url` - Product image filename

#### 3. **sizes**
Available shoe sizes
- `size_id` - Primary key
- `size_label` - Size label (36, 37, 38, 39, 40, 41)

#### 4. **variant_sizes**
Stock matrix (variant × size combinations)
- `variant_id` - Foreign key to product_variants
- `size_id` - Foreign key to sizes
- `stock_quantity` - Available quantity
- `available` - Boolean availability flag

#### 5. **sales**
Sales transactions
- `sale_id` - Primary key
- `customer_name` - Customer name
- `location` - City/location
- `payment_method` - Payment type
- `sale_date` - Transaction timestamp

#### 6. **sale_line_item**
Individual items in each sale
- `line_item_id` - Primary key
- `sale_id` - Foreign key to sales
- `variant_id` - Foreign key to product_variants
- `quantity` - Number of items
- `unit_price` - Price per unit (may include discounts)

---

## 📈 Sales Data Characteristics

### Temporal Distribution (May 2024 - November 2024)

| Month | Sales Count | Pattern |
|-------|-------------|---------|
| **May 2024** | 140 | Spring baseline |
| **June 2024** | 150 | Summer pickup |
| **July 2024** | 180 | Peak summer + July 4th spike |
| **August 2024** | 170 | Back-to-school season |
| **September 2024** | 160 | Fall transition |
| **October 2024** | 170 | Halloween spike |
| **November 2024** | 200 | Black Friday boost |

### Realistic Patterns Built Into Data

**Sales Volume Patterns:**
- 📅 **Weekends**: 6-8 sales/day
- 📅 **Weekdays**: 4-5 sales/day
- 🎆 **July 4th**: 12 sales on that day
- 🎃 **Halloween**: 10 sales on Oct 31
- 🛍️ **Black Friday period**: 15-20 sales/day

**Product Popularity:**
- 70% of sales are popular variants (1, 3, 7, 11, 14)
- 30% distributed across other variants

**Purchase Behavior:**
- 80% single-item purchases
- 15% two-item purchases
- 5% three or more items

**Pricing:**
- Regular prices most of the year
- 10-20% Black Friday discounts (Nov 15-30)

**Geographic Distribution:**
- 27 major US cities represented
- Even distribution across locations

**Payment Methods:**
- Credit Card
- Debit Card
- PayPal
- Cash
- Apple Pay

## Key Features of the data inserted:
**~1000 Sales distributed across 6 months with:**
- May 2025: 140 sales (spring baseline)
-   June 2025: 150 sales (summer starts)
-   July 2025: 180 sales (peak summer + July 4th spike)
-   August 2025: 170 sales (back-to-school season)
-   September 2025: 160 sales (fall season)
-   October 2025: 170 sales (Halloween spike)
-   November 2025: 200 sales (Black Friday boost)
**Realistic Patterns:**
-   Higher sales on weekends (6-8 sales/day vs 4-5 weekdays)
-   Seasonal spikes (July 4th, back-to-school, Black Friday)
-   70% of sales focus on popular variants (1, 3, 7, 11, 14)
-   80% single-item purchases, 15% two items, 5% three items
-   Black Friday discounts (10-20% off in mid-November)
-   Multiple payment methods and locations across 27 US cities
**Business Intelligence Ready:**
-   Top selling products analysis
-   Revenue trends by month
-   Average order value tracking
-   Customer location patterns
-   Payment method preferences
-   Seasonal sales patterns
---

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
    - ./backend/mcps/db_analytics/db/schema.sql:/docker-entrypoint-initdb.d/00-schema.sql
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

---

## 🎯 Business Intelligence Use Cases

### 1. **Sales Forecasting**
Use monthly trends to predict future performance

### 2. **Inventory Management**
Track stock levels and identify replenishment needs

### 3. **Customer Behavior Analysis**
Understand purchase patterns, location preferences, payment methods

### 4. **Seasonal Planning**
Identify peak periods and plan marketing campaigns

### 5. **Product Performance**
Determine best/worst sellers for merchandising decisions

### 6. **Revenue Optimization**
Analyze pricing strategies and discount effectiveness

### 7. **Geographic Expansion**
Identify high-performing markets for expansion

---

## 📝 Notes

- All dates are in 2025 (May - November)
- Sales hours range from 9 AM to 8 PM
- Stock quantities are initialized but don't automatically decrement with sales
- Prices include Black Friday discounts where applicable
- Foreign key constraints ensure data integrity

