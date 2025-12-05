import logging
logger = logging.getLogger(__name__)


from mcps.analytics.operations.data_reports import get_top_selling_products, get_size_mix, get_revenue_qoq_comparison, get_variant_performance, get_aov_over_time, get_top_products_with_trends_over_time, get_revenue_over_time, data_analytics_module_info



def data_reports_mgr(operation_query: dict):
    """
    Manage and route data metrics operations based on the operation_query.
    """

    if operation_query["report_type"]  == "data_analytics_module_info":
        return data_analytics_module_info(operation_query)

    elif operation_query["report_type"]  == "top_selling_products":
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
    

    
    
