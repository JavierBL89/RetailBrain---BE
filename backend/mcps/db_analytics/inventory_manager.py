import sys
import os
from pathlib import Path


from backend.mcps.db_analytics.db.init_db import get_db_connection

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
                        variant["category"],
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
                        variant_metadata = {
                            "variant_id": variant_id,
                            "brand": variant.get("brand"),
                            "category": variant.get("category"),
                            "color": variant.get("color"),
                            "material": variant.get("material"),
                            "price":variant.get("price"),
                            "heel_type": variant.get("metadata").get("heel_type"),
                            "heel_height": variant.get("metadata").variant.get("heel_height"),
                            "tags_string": variant.get("metadata").variant.get("tags_string"),
                            "occasion": variant.get("metadata").variant.get("occasion")
                            }                       
                     
                # push variant to list for return
                variants_metadata_list.append(variant_metadata)
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        print("Error inserting product:", e)

    finally:
        db_conn.close()

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


def fetch_products_by_product_id_sql(product_ids):
    """
    Fetch product details from the SQL database based on a list of product product_ids.
    """

    # FIX: product_ids must be the inner list, not the outer wrapper
    if isinstance(product_ids, list) and len(product_ids) == 1 and isinstance(product_ids[0], list):
        product_ids = product_ids[0]

    if not product_ids:
        print("⚠ No product_ids passed to SQL fetch.")
        return []

    db_conn = get_db_connection()

    placeholders = ",".join(["%s"] * len(product_ids))
    query = f"""
        SELECT 
            v.variant_id,
            v.product_id
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
        cur.execute(query, product_ids)
        rows = cur.fetchall()

    db_conn.close()
    products = {}
    for r in rows:
        pid = r[0]

        if pid not in products:
            products[pid] = {
                "product_id": r[0],
                "sku": r[1],
                "name": r[2],
                "description": r[3],
                "category": r[4],
                "material": r[5],
                "gender": r[6],
                "brand": r[7],
                "tags_string": r[8],
                "variants": []
            }

        variant = {
            "variant_id": r[9],
            "variant_sku": r[10],
            "color": r[11],
            "price": float(r[12]) if r[12] else None,
            "image_url": r[13]
        }

        if r[9] is not None:
            products[pid]["variants"].append(variant)

    return list(products.values())
