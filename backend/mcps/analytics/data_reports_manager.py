import logging
logger = logging.getLogger(__name__)


from mcps.analytics.operations.data_reports import get_top_selling_products, get_size_mix, get_revenue_qoq_comparison, get_variant_performance, get_aov_over_time, get_top_products_with_trends_over_time, get_revenue_over_time



def data_reports_mgr(operation_query: dict):
    """
    Manage and route data metrics operations based on the operation_query.
    """

    if operation_query["report_type"]  == "top_selling_products":
        return get_top_selling_products(operation_query)
    
    elif operation_query["report_type"]  == "top_products_with_trends_over_time":
        return get_top_products_with_trends_over_time(operation_query)  
    
    elif operation_query["report_type"]  == "size_mix":
        return get_size_mix(operation_query)

    elif operation_query["report_type"]  == "revenue_qoq_comparison":
        return get_revenue_qoq_comparison(operation_query)
    
    elif operation_query["report_type"]  == "revenue_over_time":
        return get_revenue_over_time(operation_query)
    
    elif operation_query["report_type"]  == "variant_performance":
        return get_variant_performance(operation_query)
    
    elif operation_query["report_type"]  == "aov_over_time":
        return get_aov_over_time(operation_query)
    


def data_analytics_module_info():
    """
    Returns metadata about the sales analytics module for MCP discovery.
    Includes available functions, descriptions, grouping modes, and filters.
    """
    return {
        "module": "sales_analytics",
        "description": "Analytics module for retrieving sales metrics, trends, and performance insights.",
        "group_by_options": ["day", "week", "month", "quarter"],
        "supported_filters": [
            "brand", 
            "category", 
            "sku", 
            "color", 
            "material",
            "customer_city",
            "payment_method"
        ],
        "functions": [
            {
                "name": "get_top_selling_products",
                "description": "Returns top-selling product variants over a date range with sales and revenue totals.",
                "params": {
                    "date_from": "Start date (YYYY-MM-DD)",
                    "date_to": "End date (YYYY-MM-DD)",
                    "threshold": "Minimum units sold",
                    "limit": "Maximum number of results",
                    "group_by": "Optional time grouping"
                }
            },
            {
                "name": "get_revenue_over_time",
                "description": "Returns revenue grouped by day/week/month/quarter.",
                "params": {
                    "date_from": "Start date",
                    "date_to": "End date",
                    "group_by": "Grouping mode",
                    "threshold": "Minimum revenue threshold",
                    "limit": "Max periods to return"
                }
            },
            {
                "name": "get_sales_over_time",
                "description": "Returns sales units + revenue grouped over time.",
                "params": {
                    "date_from": "Start date",
                    "date_to": "End date",
                    "group_by": "Grouping mode"
                }
            },
            {
                "name": "get_revenue_qoq_comparison",
                "description": "Returns quarter-over-quarter revenue and growth rate.",
                "params": {
                    "date_from": "Start date",
                    "date_to": "End date",
                    "filters": "Optional brand/category/city/material filters"
                }
            },
            {
                "name": "get_top_products_with_trends_over_time",
                "description": "Returns top products and their sales trends across periods.",
                "params": {
                    "date_from": "Start date",
                    "date_to": "End date",
                    "limit": "Number of top products",
                    "threshold": "Minimum units sold",
                    "group_by": "Time grouping",
                    "filters": "Optional filters"
                }
            },
            {"name": "get_size_mix", "description": "Returns size mix distribution (to be implemented)"},
            {"name": "get_variant_performance", "description": "Returns variant performance metrics (to be implemented)"},
            {"name": "get_aov_over_time", "description": "Returns average order value over time (to be implemented)"},
            {"name": "get_sales_data", "description": "Raw dump of the sales table"},
            {"name": "get_sales_line_items_data", "description": "Raw dump of sale_line_items"},
            {"name": "get_product_variants_data", "description": "Raw dump of product_variants"},
            {"name": "get_cities_metadata", "description": "List of all city-level metadata"},
            {"name": "get_payment_methods_data", "description": "List of payment methods"}
        ]
    }

    
