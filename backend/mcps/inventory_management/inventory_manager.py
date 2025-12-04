import sys
import os
from pathlib import Path


from mcps.db.init_db import get_db_connection

def inventory_manager(user_query: list | dict = None, action: str = None) -> dict:
    """

    """

    if action == "describe":
        return inv_mang_module_info()

    if isinstance(user_query, str):
        import json
        user_query =[user_query]

    match action:
        case "delete_variant_by_sku":
            return delete_variants_by_sku_sql(user_query)
        case "delete_product_by_id":
            return delete_products_by_id_sql(user_query)
        case "get_low_stock_product_variants":
            return get_low_stock_product_variants(user_query)
        

def inv_mang_module_info():
    """
    Returns structured info about the inventory manager module.
    Helps the LLM decide which action to call.
    """
    return {
        "module": "inventory_manager",
        "description": "SQL-backed inventory management: products, variants, stock, sizes.",
        "actions": {
            "insert_new_product_sql": "Insert one or more products with variants and sizes.",
            "update_products_sql": "(NO AVAILABLE) Update product or variant information.",
            "delete_products_by_id_sql": "(NO AVAILABLE) Delete products and cascade-remove variants + stocks.",
            "delete_variant_by_sku": "(NO AVAILABLE) Delete one or more variants based on SKU.",
            "fetch_products_by_product_id_sql": "(NO AVAILABLE)Fetch product + variant details by product_id.",
            "fetch_variants_by_variant_id_sql": "Fetch one or more variants (with image).",
            "fetch_all_product_variants": "Return all variants in database.",
            "get_products_variants_with_images": "(NO AVAILABLE)Fetch variants + base64 images.",
            "get_low_stock_product_variants": "Return variants where total stock < threshold.",
            "describe": "List all available actions and module description."
        }
    }



def insert_new_product_sql(products_data: dict | list ) -> list:
    """
    Accepts either:
    - a single product dict
    - a list of product dicts
    
    Returns:
        list of inserted product_ids
    """

    # Normalize to list
    if isinstance(products_data, dict):
        products_data = [products_data]
    
    db_conn = get_db_connection()

    # Define SQL queries needed
    product_query = """
        INSERT INTO products (sku, category, brand)
        VALUES (%s, %s, %s )
        RETURNING product_id;
    """

    variant_query = """
        INSERT INTO product_variants (product_id, variant_sku, name, description, category, color, material, gender, brand, price, image_url, tags_string)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING variant_id;
    """
    
    size_insert_query = """
        INSERT INTO sizes (size_label)
        VALUES (%s)
        ON CONFLICT (size_label) DO NOTHING
        RETURNING size_id;
    """

    size_lookup_query = "SELECT size_id FROM sizes WHERE size_label=%s;"

    variant_size_query = """
        INSERT INTO variant_sizes (variant_id, size_id, stock_quantity, available)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (variant_id, size_id)
        DO UPDATE SET stock_quantity = EXCLUDED.stock_quantity,
                      available = EXCLUDED.available;
    """
    variant_metadata = """
    INSERT INTO variant_metadata 
    (variant_id, brand, category, color, material, heel_type, heel_height, tags_string, occasion)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print(products_data)
    inserter_product_ids = []
    inserted_variant_ids = []
    variants_metadata_list = []

    try:
        with db_conn.cursor() as cur:
            for product_data in products_data:
                    
                # 1. Insert Product
                p = product_data
                cur.execute(product_query, (
                    p["sku"],  p["category"], p["brand"]
                ))
                product_id = cur.fetchone()[0]
                inserter_product_ids.append(product_id)

                # 2. Insert Variants
                for variant in product_data["variants"]:
                    cur.execute(variant_query, (
                        product_id,
                        variant["variant_sku"],
                        variant["name"],
                        variant["description"],
                        product_data["category"],
                        variant["color"],
                        variant["material"],
                        variant["gender"],
                        variant["brand"],
                        variant["price"],
                        variant["image_url"],
                        variant.get("tags_string", "")
                    ))
                    variant_id = cur.fetchone()[0]
                    inserted_variant_ids.append(variant_id)

                    # 3. Insert sizes for this variant
                    for s in variant["sizes"]:

                        # ensure size exists in sizes table
                        cur.execute(size_insert_query, (s["size_label"],))
                        res = cur.fetchone()
                        if res:
                            size_id = res[0]
                        else:
                            cur.execute(size_lookup_query, (s["size_label"],))
                            size_id = cur.fetchone()[0]

                        # 4. Insert variant-size stock info
                        cur.execute(variant_size_query, (
                            variant_id,
                            size_id,
                            s["stock_quantity"],
                            s["available"]
                        ))

                        # 5. store variant metadata to pass to vector DB
                        meta = variant.get("metadata", {})
                        variant_metadata = {
                            "variant_id": variant_id,
                            "brand": variant.get("brand"),
                            "category": p.get("category"),  # product-level category
                            "color": variant.get("color"),
                            "material": variant.get("material"),
                            "price": variant.get("price"),
                            "heel_type": meta.get("heel_type"),
                            "heel_height": meta.get("heel_height"),
                            "tags_string": variant.get("tags_string"),
                            "occasion": meta.get("occasion")
                            }                       
                     
                    # push variant to list for return
                    variants_metadata_list.append(variant_metadata)
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        error_msg = f"Error inserting product: {str(e)}"
        raise Exception(error_msg)  # Re-raise so outer catch block can return it
        
    finally:
        db_conn.close()

    print({"Products added to SQL with ids ": inserter_product_ids})
    print({"Variants added to SQL with ids ": inserted_variant_ids})
    return {
        "status": "success",
        "SQL_inserted_product_ids": inserter_product_ids,
        "SQL_inserted_product_variants_ids": inserted_variant_ids,
        "variants_per_product": variants_metadata_list
    }


def update_products_sql(products_data: list, mode: str = "patch") -> dict:
    """
    Update existing products and their variants in the SQL database.
    """
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cur:

            for product in products_data:

                # -----------------------------
                # 1. PRODUCT UPDATE
                # -----------------------------

                if mode == "replace":
                    # FULL UPDATE
                    cur.execute("""
                        UPDATE products
                        SET 
                            sku = %s,
                            category = %s,
                            brand = %s
                        WHERE product_id = %s;
                    """, (
                        product.get("sku"),
                        product.get("category"),
                        product.get("brand"),
                        product["product_id"]
                    ))
                else:
                    # PATCH UPDATE
                    cur.execute("""
                        UPDATE products
                        SET 
                            sku = COALESCE(%s, sku),
                            category = COALESCE(%s, category),
                            brand = COALESCE(%s, brand)
                        WHERE product_id = %s;
                    """, (
                        product.get("sku"),
                        product.get("category"),
                        product.get("brand"),
                        product["product_id"]
                    ))

                # -----------------------------
                # 2. VARIANTS UPDATE
                # -----------------------------
                for variant in product.get("variants", []):

                    if mode == "replace":
                        cur.execute("""
                            UPDATE product_variants
                            SET
                                variant_sku = %s,
                                name = %s,
                                description = %s,
                                category = %s,
                                color = %s,
                                material = %s,
                                gender = %s,
                                brand = %s,
                                price = %s,
                                image_url = %s,
                                tags_string = %s
                            WHERE variant_id = %s;
                        """, (
                            variant.get("variant_sku"),
                            variant.get("name"),
                            variant.get("description"),
                            variant.get("category"),
                            variant.get("color"),
                            variant.get("material"),
                            variant.get("gender"),
                            variant.get("brand"),
                            variant.get("price"),
                            variant.get("image_url"),
                            variant.get("tags_string"),
                            variant["variant_id"]
                        ))

                    else:
                        cur.execute("""
                            UPDATE product_variants
                            SET
                                variant_sku = COALESCE(%s, variant_sku),
                                name = COALESCE(%s, name),
                                description = COALESCE(%s, description),
                                category = COALESCE(%s, category),
                                color = COALESCE(%s, color),
                                material = COALESCE(%s, material),
                                gender = COALESCE(%s, gender),
                                brand = COALESCE(%s, brand),
                                price = COALESCE(%s, price),
                                image_url = COALESCE(%s, image_url),
                                tags_string = COALESCE(%s, tags_string)
                            WHERE variant_id = %s;
                        """, (
                            variant.get("variant_sku"),
                            variant.get("name"),
                            variant.get("description"),
                            variant.get("category"),
                            variant.get("color"),
                            variant.get("material"),
                            variant.get("gender"),
                            variant.get("brand"),
                            variant.get("price"),
                            variant.get("image_url"),
                            variant.get("tags_string"),
                            variant["variant_id"]
                        ))

                    # -----------------------------
                    # 3. VARIANT-SIZE UPDATE
                    # -----------------------------
                    for s in variant.get("sizes", []):

                        cur.execute("""
                            UPDATE variant_sizes
                            SET
                                stock_quantity = COALESCE(%s, stock_quantity),
                                available = COALESCE(%s, available)
                            WHERE variant_id = %s AND size_id = %s;
                        """, (
                            s.get("stock_quantity"),
                            s.get("available"),
                            variant["variant_id"],
                            s["size_id"]
                        ))

        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        db_conn.close()

    return {"status": "success"}


def delete_products_by_id_sql(delete_request: dict) -> dict:
    """
    Delete products, variants, sizes, and variant-size relations based on provided IDs.
    """
    db_conn = get_db_connection()

    deleted_products = []
    deleted_variants = []
    deleted_sizes = []
    deleted_variant_sizes = []

    try:
        with db_conn.cursor() as cur:

            # -------------------------
            # Delete products
            # -------------------------
            for pid in delete_request.get("products", []):
                cur.execute("""
                    DELETE FROM products
                    WHERE product_id = %s
                    RETURNING product_id;
                """, (pid,))
                result = cur.fetchone()
                if result:
                    deleted_products.append(result[0])

            # -------------------------
            # Delete variants
            # -------------------------
            for vid in delete_request.get("variants", []):
                cur.execute("""
                    DELETE FROM product_variants
                    WHERE variant_id = %s
                    RETURNING variant_id;
                """, (vid,))
                result = cur.fetchone()
                if result:
                    deleted_variants.append(result[0])

            # -------------------------
            # Delete sizes
            # -------------------------
            for sid in delete_request.get("sizes", []):
                cur.execute("""
                    DELETE FROM sizes
                    WHERE size_id = %s
                    RETURNING size_id;
                """, (sid,))
                result = cur.fetchone()
                if result:
                    deleted_sizes.append(result[0])

            # -------------------------
            # Delete variant-size relations
            # -------------------------
            for vs in delete_request.get("variant_sizes", []):
                cur.execute("""
                    DELETE FROM variant_sizes
                    WHERE variant_id = %s AND size_id = %s
                    RETURNING variant_id, size_id;
                """, (vs["variant_id"], vs["size_id"]))
                result = cur.fetchone()
                if result:
                    deleted_variant_sizes.append({"variant_id": result[0], "size_id": result[1]})

        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        db_conn.close()

    return {
        "status": "success",
        "deleted_products": deleted_products,
        "deleted_variants": deleted_variants,
        "deleted_sizes": deleted_sizes,
        "deleted_variant_sizes": deleted_variant_sizes
    }


def delete_variants_by_sku_sql(delete_request: dict | list) -> dict:
    """
    Delete products and their variants based on provided SKUs.
    """
    db_conn = get_db_connection()

    deleted_variants = []
    try:
        with db_conn.cursor() as cur:

            # -------------------------
            # Delete variants
            # -------------------------
            for vid in delete_request.get("variant_skus", []):
                cur.execute("""
                    DELETE FROM product_variants
                    WHERE variant_sku = %s
                    RETURNING variant_sku;
                """, (vid,))
                result = cur.fetchone()
                if result:
                    deleted_variants.append(result[0])

        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        db_conn.close()

    return {
        "status": "success",
        "deleted_variants": deleted_variants,
    }


def fetch_variants_by_variant_id_sql(variant_ids):
    if not variant_ids:
        return []

    # Normalize input
    if isinstance(variant_ids, set):
        variant_ids = list(variant_ids)
        
    # Guarantee variant_ids is a flat list of strings
    if isinstance(variant_ids, str):
        variant_ids = [variant_ids]
    elif isinstance(variant_ids, list):
        flat = []
        for x in variant_ids:
            if isinstance(x, list):
                flat.extend(x)
            else:
                flat.append(x)
        variant_ids = flat
    else:
        raise ValueError(f"variant_ids has invalid type: {type(variant_ids)}")

    # Convert all to strings
    variant_ids = [str(v) for v in variant_ids]
    print("Variant Ids to be fetched", variant_ids)
    
    variants = []

    try:
        db_conn = get_db_connection()
        placeholders = ",".join(["%s"] * len(variant_ids))

        query = f"""
            SELECT 
                v.variant_id,
                v.product_id,
                v.variant_sku,
                v.name,
                v.description,
                v.category,
                v.color,
                v.material,
                v.gender,
                v.brand,
                v.price,
                v.image_url,
                v.tags_string
            FROM product_variants v
            WHERE v.variant_id IN ({placeholders})
        """
        
        with db_conn.cursor() as cur:
            cur.execute(query, variant_ids)
            rows = cur.fetchall()

        db_conn.close()

        for r in rows:
            variant = {
                "variant_id": r[0],
                "product_id": r[1],
                "variant_sku": r[2],
                "name": r[3],
                "description": r[4],
                "category": r[5],
                "color": r[6],
                "material": r[7],
                "gender": r[8],
                "brand": r[9],
                "price": float(r[10]) if r[10] is not None else None,
                "image": r[11],
                "tags_string": r[12]
            }
            filename = variant["image"]

            # Ignore external URLs (like example.com)
            if isinstance(filename, str) and not filename.startswith("http"):
                variant["image_base64"] = encode_image_base64(filename)
            else:
                variant["image_base64"] = None

            variants.append(variant)
    except Exception as e:
        print("Error occur whem mapping variant. Error", e)
        return []
    
    # Create lookup table to preserve the original RANKING order
    order_map = {vid: index for index, vid in enumerate(variant_ids)}
    # Sort SQL variants by that order
    variants = sorted(variants, key=lambda v: order_map.get(str(v["variant_id"]), 999))
    return {"variants": variants}


def fetch_all_product_variants():
    """
    Fetch all product variants from the database.
    """
    query = """
        SELECT *
        FROM product_variants
    """
    
    # Use a context manager to ensure the connection is closed
    with get_db_connection() as db_conn:
        with db_conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    
    return rows


def get_products_variants_with_images():
    """
    Fetch all product variants and encode their images in base64.
    """
    rows = fetch_all_product_variants()
    products = []

    for r in rows:
        product = {
            "id": r[0],
            "variant_id": r[1],
            "sku": r[2],
            "name": r[3],
            "description": r[4],
            "category": r[5],
            "color": r[6],
            "material": r[7],
            "gender": r[8],
            "brand": r[9],
            "price": r[10],
            "image": r[11],
            "keywords": r[12],
            "created_at": r[13],
            "updated_at": r[14],
        }

        filename = product["image"]

        # Ignore external URLs (like example.com)
        if isinstance(filename, str) and not filename.startswith("http"):
            product["image_base64"] = encode_image_base64(filename)
        else:
            product["image_base64"] = None

        products.append(product)

    return products


def get_low_stock_product_variants(user_query: dict):
    """
    Returns a list of product variants where total stock (sum of all sizes)
    is below the provided threshold.
    """
    threshold = user_query.get("stock_threshold")
    
    db_conn = get_db_connection()
    try:
        with db_conn.cursor() as cur:
            # Step 1: Get list of low stock variant IDs
            cur.execute("""
                SELECT pv.variant_id
                FROM product_variants pv
                JOIN variant_sizes vs ON pv.variant_id = vs.variant_id
                GROUP BY pv.variant_id
                HAVING SUM(vs.stock_quantity) < %s
            """, (threshold,))
            
            low_stock_ids = [row[0] for row in cur.fetchall()]
            
            if not low_stock_ids:
                return {
                    "status": "success",
                    "variants": []
                }
            
            # Step 2: Get detailed size breakdown
            placeholders = ",".join(["%s"] * len(low_stock_ids))
            cur.execute(f"""
                SELECT 
                    pv.variant_id,
                    pv.variant_sku,
                    pv.name AS variant_name,
                    s.size_label,
                    vs.stock_quantity
                FROM product_variants pv
                JOIN variant_sizes vs ON pv.variant_id = vs.variant_id
                JOIN sizes s ON vs.size_id = s.size_id
                WHERE pv.variant_id IN ({placeholders})
                ORDER BY pv.variant_id, s.size_label;
            """, low_stock_ids)
            
            rows = cur.fetchall()
            
            # Step 3: Organize results
            variants = {}
            for row in rows:
                v_id = row[0]
                if v_id not in variants:
                    variants[v_id] = {
                        "variant_id": row[0],
                        "variant_sku": row[1],
                        "variant_name": row[2],
                        "size_breakdown": [],
                        "total_stock": 0
                    }
                
                variants[v_id]["size_breakdown"].append({
                    "size_label": row[3],
                    "stock_quantity": row[4]
                })
                
                variants[v_id]["total_stock"] += row[4]
            
            return {
                "status": "success",
                "variants": list(variants.values()),
                "total_variants": len(variants),
                "grand_total_stock": sum(v["total_stock"] for v in variants.values())
            }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    finally:
        db_conn.close()


###  Heper functions ###
import base64
from pathlib import Path

def encode_image_base64(filename: str) -> str:
    image_path = Path("backend/static/images") / filename
    if image_path.exists():
        return base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return None