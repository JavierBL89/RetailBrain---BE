

from pathlib import Path
import json
from decimal import Decimal
from datetime import date, datetime

from mcps.db.init_db import get_db_connection


GROUP_BY_MAP = {
        "day":      "TO_CHAR(s.sale_date, 'YYYY-MM-DD')",
        "week":     "TO_CHAR(s.sale_date, 'IYYY-IW')",
        "month":    "TO_CHAR(s.sale_date, 'YYYY-MM')",
        "quarter":  "TO_CHAR(s.sale_date, 'YYYY-Q')"
    }




def get_top_selling_products(user_query: dict):
    """
    Fetch top selling products data over a period of time.
    returns:
        List of DICTIONARIES
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    group_by_expr = GROUP_BY_MAP.get(user_query.get("group_by", "month"), "TO_CHAR(s.sale_date, 'YYYY-MM')")

    cursor.execute(
        f"""
        SELECT
            v.variant_id,
            v.variant_id,
            v.name AS variant_name,
            p.sku,
            p.brand,
            p.category,
            v.color,
            SUM(sli.quantity) AS total_sold,
            SUM(sli.quantity * sli.unit_price) AS total_revenue,
            v.image_url
        FROM sale_line_item sli
        JOIN sales s               ON s.sale_id = sli.sale_id
        JOIN product_variants v    ON sli.variant_id = v.variant_id
        JOIN products p            ON p.product_id = v.product_id
        WHERE s.sale_date BETWEEN %(date_from)s AND %(date_to)s
        GROUP BY v.variant_id, variant_name, p.sku, p.brand, p.category, v.color, v.image_url
        HAVING SUM(sli.quantity) >= %(threshold)s
        ORDER BY total_sold DESC
        LIMIT %(limit)s;
        """,
        {
            "date_from": user_query.get("date_from"),
            "date_to": user_query.get("date_to"),
            "threshold": user_query.get("threshold", 1),
            "limit": user_query.get("limit", 10)        
        }
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_revenue_over_time(user_query: dict):
    """
    Fetch revenue over time data from the database.
    returns:
    List of DICTIONARIES
    """
    group_by_expr = GROUP_BY_MAP.get(user_query.get("group_by", "month"), "TO_CHAR(s.sale_date, 'YYYY-MM')")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( 
        f"""
        SELECT
            {group_by_expr} AS period,
            SUM(sli.quantity * sli.unit_price) AS revenue
        FROM sale_line_item sli
        JOIN sales s ON s.sale_id = sli.sale_id
        JOIN product_variants v ON v.variant_id = sli.variant_id
        JOIN products p ON p.product_id = v.product_id
        WHERE s.sale_date BETWEEN %(date_from)s AND %(date_to)s
        GROUP BY period
        HAVING SUM(sli.quantity * sli.unit_price) >= %(threshold)s
        ORDER BY period
        LIMIT %(limit)s;
        """,
        {
            "date_from": user_query.get("date_from"),
            "date_to": user_query.get("date_to"),
            "threshold": user_query.get("threshold", 1),
            "limit": user_query.get("limit", 10)        
        }
    )
    
    # Convert to dictionaries
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    cursor.close()
    conn.close()
    # Apply JSON serialization
    return make_json_serializable(results)

def get_revenue_qoq_comparison(user_query: dict):    
    """
    Returns quarterly revenue totals + QoQ growth rate.
    
    Example return:
    [
        {"quarter_label": "2025-Q2", "revenue": 48931.76, "growth_rate": None},
        {"quarter_label": "2025-Q3", "revenue": 51290.11, "growth_rate": 0.048},
        {"quarter_label": "2025-Q4", "revenue": 57100.44, "growth_rate": 0.113}
    ]
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    date_from = user_query.get("date_from")
    date_to   = user_query.get("date_to")
    filters   = user_query.get("filters", {})

    # ===== Build dynamic filter SQL =====
    filter_sql, filter_params = build_filters(filters)
    filter_sql = f" AND {filter_sql}" if filter_sql else ""

    # ===== SQL Query =====
    sql = f"""
        WITH revenue_quarters AS (
            SELECT
                DATE_TRUNC('quarter', s.sale_date) AS quarter_start,
                TO_CHAR(s.sale_date, 'YYYY-"Q"Q') AS quarter_label,
                SUM(sli.quantity * sli.unit_price) AS revenue
            FROM sales s
            JOIN sale_line_item sli ON s.sale_id = sli.sale_id
            JOIN product_variants v ON v.variant_id = sli.variant_id
            JOIN products p ON p.product_id = v.product_id
            WHERE s.sale_date BETWEEN %(date_from)s AND %(date_to)s
            {filter_sql}
            GROUP BY quarter_start, quarter_label
            ORDER BY quarter_start
        )
        SELECT
            quarter_label,
            revenue,
            ROUND(
                (revenue - LAG(revenue) OVER (ORDER BY quarter_start)) /
                NULLIF(LAG(revenue) OVER (ORDER BY quarter_start), 0),
                4
            ) AS growth_rate
        FROM revenue_quarters;
    """

    params = {
        "date_from": date_from,
        "date_to": date_to,
        **filter_params
    }

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    # Convert rows to list of dicts  
    return [dict(zip(colnames, row)) for row in rows]

def get_top_products_with_trends_over_time(user_query: dict):
    """
    Fetch top selling products along with their sales trends over time.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    group_expr = GROUP_BY_MAP.get(
        user_query.get("group_by", "month"),
        GROUP_BY_MAP["month"]
    )

    date_from = user_query.get("date_from")
    date_to   = user_query.get("date_to")
    limit     = user_query.get("limit", 5)
    threshold = user_query.get("threshold", 1)
    filters   = user_query.get("filters", {})

    # ----- Build Dynamic Filters -----
    filter_sql, filter_params = build_filters(filters)
    filter_sql = f" AND {filter_sql}" if filter_sql else ""

    # ===============================
    # 1️⃣ QUERY: TOP PRODUCTS
    # ===============================
    top_products_sql = f"""
        WITH top_products AS (
            SELECT
                v.variant_id,
                v.name AS variant_name,
                p.sku,
                p.brand,
                p.category,
                v.image_url,
                SUM(sli.quantity) AS total_sold,
                SUM(sli.quantity * sli.unit_price) AS total_revenue
            FROM sale_line_item sli
            JOIN sales s               ON s.sale_id = sli.sale_id
            JOIN product_variants v    ON sli.variant_id = v.variant_id
            JOIN products p            ON p.product_id = v.product_id
            WHERE s.sale_date BETWEEN %(date_from)s AND %(date_to)s
            {filter_sql}
            GROUP BY v.variant_id, variant_name, p.sku, p.brand, p.category, v.image_url
            HAVING SUM(sli.quantity) >= %(threshold)s
            ORDER BY total_sold DESC
            LIMIT %(limit)s
        )
        SELECT * FROM top_products;
    """

    params = {
        "date_from": date_from,
        "date_to": date_to,
        "limit": limit,
        "threshold": threshold,
        **filter_params
    }

    cursor.execute(top_products_sql, params)
    top_products_rows = cursor.fetchall()
    top_product_cols = [d[0] for d in cursor.description]

    top_products = [dict(zip(top_product_cols, row)) for row in top_products_rows]

    # Extract variant_ids for the trend query
    variant_ids = [row["variant_id"] for row in top_products]

    if not variant_ids:
        cursor.close()
        conn.close()
        return {"top_products": [], "trends": []}

    # ===============================
    # 2️⃣ QUERY: TRENDS FOR TOP PRODUCTS
    # ===============================
    trends_sql = f"""
        SELECT
            {group_expr} AS period,
            sli.variant_id,
            SUM(sli.quantity) AS units_sold,
            SUM(sli.quantity * sli.unit_price) AS revenue
        FROM sale_line_item sli
        JOIN sales s ON s.sale_id = sli.sale_id
        WHERE s.sale_date BETWEEN %(date_from)s AND %(date_to)s
          AND sli.variant_id = ANY(%(variant_ids)s)
        GROUP BY period, sli.variant_id
        ORDER BY period, sli.variant_id;
    """

    cursor.execute(trends_sql, {
        "date_from": date_from,
        "date_to": date_to,
        "variant_ids": variant_ids
    })

    trend_rows = cursor.fetchall()
    trend_cols = [d[0] for d in cursor.description]
    trends = [dict(zip(trend_cols, row)) for row in trend_rows]

    cursor.close()
    conn.close()

    return make_json_serializable({
        "top_products": top_products,
        "trends": trends
    })

def get_sales_over_time(user_query: dict):
    """
    Fetch sales over time data from the database.
    returns:
    List of DICTIONARIES
    """
    group_by_expr = GROUP_BY_MAP.get(user_query.get("group_by", "month"), "TO_CHAR(s.sale_date, 'YYYY-MM')")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( 
        f"""
        SELECT
            {group_by_expr} AS period,
            SUM(sli.quantity) AS units_sold,
            SUM(sli.quantity * sli.unit_price) AS revenue
        FROM sale_line_item sli
        JOIN sales s ON s.sale_id = sli.sale_id
        JOIN product_variants v ON v.variant_id = sli.variant_id
        JOIN products p ON p.product_id = v.product_id
        WHERE s.sale_date BETWEEN %(date_from)s AND %(date_to)s
        -- filters
        GROUP BY period
        ORDER BY period;
        """,
        {
            "date_from": user_query.get("date_from"),
            "date_to": user_query.get("date_to"),
            "threshold": user_query.get("threshold", 1),
            "limit": user_query.get("limit", 10)        
        }
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results



##### empty function templates
def get_size_mix():
    """
    Fetch size mix data from the database.
    """

def get_variant_performance():    
    """
    Fetch variant performance data from the database.
    """

def get_aov_over_time():
    """
    Fetch average order value over time data from the database.
    """

def get_sales_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales;")
    data = cursor.fetchall()
    conn.close()
    return data

def get_sales_line_items_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales_line_items;")
    data = cursor.fetchall()
    conn.close()
    return data

def get_product_variants_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product_variants;")
    data = cursor.fetchall()
    conn.close()
    return data

def get_cities_metadata():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cities;")
    data = cursor.fetchall()
    conn.close()
    return data 

def get_payment_methods_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payment_methods;")
    data = cursor.fetchall()
    conn.close()
    return data



#### Helper functions

def build_filters(filters: dict):
    """
    Build SQL WHERE clause parts and parameters from filters dictionary.
    """
    sql_parts = []
    params = {}

    for key, value in filters.items():
        # maps filter field → DB column
        if key in ["brand", "category", "sku"]:
            sql_parts.append(f"p.{key} = %({key})s")
        elif key in ["color", "material"]:
            sql_parts.append(f"v.{key} = %({key})s")
        elif key in ["customer_city"]:
            sql_parts.append(f"s.{key} = %({key})s")
        elif key in ["payment_method"]:
            sql_parts.append(f"s.{key} = %({key})s")
        else:
            continue
        
        params[key] = value

    return " AND ".join(sql_parts), params


def make_json_serializable(value):
    from decimal import Decimal
    from datetime import date, datetime

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, dict):
        return {k: make_json_serializable(v) for k, v in value.items()}

    if isinstance(value, list):
        return [make_json_serializable(v) for v in value]

    return value