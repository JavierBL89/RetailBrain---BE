import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

from mcps.analytics.operations.data_reports import (
    get_top_selling_products,
    get_size_mix,
    get_revenue_qoq_comparison,
    get_variant_performance,
    get_aov_over_time,
    get_top_products_with_trends_over_time,
    get_revenue_over_time,
)
from mcps.analytics.report_formatter import format_report
from mcps.analytics.claude_client import generate_report_with_claude


def data_reports_mgr(operation_query: dict) -> Dict[str, Any]:
    """Manage and route data metrics operations, optionally using Claude for summaries.

    Returns a dict with keys: `status`, `data` (structured result), and `message` (human-readable summary).
    If `operation_query` contains `llm_provider: 'claude'`, the function will call the Claude client
    to produce the `message` from the structured `data`.
    """

    report_type = operation_query.get("report_type")
    if not report_type:
        return {"status": "error", "message": "Missing report_type in operation_query", "data": None}

    result = None
    try:
        if report_type == "top_selling_products":
            result = get_top_selling_products(operation_query)

        elif report_type == "top_products_with_trends_over_time":
            result = get_top_products_with_trends_over_time(operation_query)

        elif report_type == "size_mix":
            result = get_size_mix(operation_query)

        elif report_type == "revenue_qoq_comparison":
            result = get_revenue_qoq_comparison(operation_query)

        elif report_type == "revenue_over_time":
            result = get_revenue_over_time(operation_query)

        elif report_type == "variant_performance":
            result = get_variant_performance(operation_query)

        elif report_type == "aov_over_time":
            result = get_aov_over_time(operation_query)

        else:
            return {"status": "error", "message": f"Unknown report_type: {report_type}", "data": None}

    except Exception as e:
        logger.exception("Error generating report data for %s", report_type)
        return {"status": "error", "message": str(e), "data": None}

    # Decide whether to use an LLM provider for the human-friendly message
    llm_provider = operation_query.get("llm_provider")
    tone = operation_query.get("tone", "friendly")
    message = None
    if llm_provider == "claude":
        try:
            message = generate_report_with_claude(report_type, result, tone=tone)
        except Exception as e:
            logger.exception("Claude generation failed for %s: %s", report_type, e)
            # fall back to local formatter when Claude fails
            try:
                message = format_report(report_type, result, operation_query)
            except Exception:
                message = "(Could not generate a summary.)"
    else:
        try:
            message = format_report(report_type, result, operation_query)
        except Exception:
            logger.exception("Local formatting failed for %s", report_type)
            message = "(Could not generate a summary.)"

    return {"status": "ok", "data": result, "message": message}
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
        result = get_top_products_with_trends_over_time(operation_query)
        return result  # ← Make sure this return is here!
    
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
    

    
    
