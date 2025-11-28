from typing import Any, Dict, List


def _safe_get_top(items: List[Dict], key_candidates: List[str], limit: int = 3):
    if not items:
        return []
    key = None
    for k in key_candidates:
        if any(k in it for it in items):
            key = k
            break
    if key is None:
        return items[:limit]
    try:
        return sorted(items, key=lambda x: float(x.get(key, 0)), reverse=True)[:limit]
    except Exception:
        return items[:limit]


def format_top_selling(report: Any, params: Dict) -> str:
    items = report if isinstance(report, list) else report.get("items", []) if isinstance(report, dict) else []
    top = _safe_get_top(items, ["units_sold", "sold", "quantity", "sales"], limit=3)
    if not top:
        return "No top selling products found for the requested period."
    parts = []
    for it in top:
        name = it.get("product_name") or it.get("name") or it.get("title") or "Unknown product"
        qty = it.get("units_sold") or it.get("sold") or it.get("quantity") or it.get("sales") or "an unknown amount"
        parts.append(f"{name} ({qty} units)")
    period = params.get("period") or params.get("date_range") or "the period"
    return f"Top sellers for {period}: " + ", ".join(parts) + "."


def format_revenue_qoq(report: Any, params: Dict) -> str:
    if not isinstance(report, dict):
        return "Couldn't generate revenue comparison — unexpected data format."
    prev = report.get("previous_period")
    curr = report.get("current_period")
    if prev is None or curr is None:
        return "Insufficient data for quarter-on-quarter revenue comparison."
    try:
        change = ((float(curr) - float(prev)) / (abs(float(prev)) or 1)) * 100
        trend = "up" if change > 0 else "down" if change < 0 else "flat"
        return f"Revenue is {trend} {abs(round(change,1))}% vs previous quarter (from {prev} to {curr})."
    except Exception:
        return "Couldn't compute revenue percentage change due to unexpected values."


def format_time_series(report: Any, params: Dict) -> str:
    series = None
    if isinstance(report, dict):
        series = report.get("series") or report.get("data")
    elif isinstance(report, list):
        series = report
    if not series or len(series) < 2:
        return "Not enough data points to create a time-series summary."
    try:
        first = float(series[0].get("value", series[0]) if isinstance(series[0], dict) else series[0])
        last = float(series[-1].get("value", series[-1]) if isinstance(series[-1], dict) else series[-1])
        change = ((last - first) / (abs(first) or 1)) * 100
        direction = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
        return f"Values {direction} by {abs(round(change,1))}% from {first} to {last} over the selected period."
    except Exception:
        return "Couldn't summarize the time-series due to unexpected format."


def format_report(report_type: str, report: Any, params: Dict = None) -> str:
    params = params or {}
    try:
        if report_type == "top_selling_products":
            return format_top_selling(report, params)
        if report_type == "revenue_qoq_comparison":
            return format_revenue_qoq(report, params)
        if report_type in ("revenue_over_time", "aov_over_time", "top_products_with_trends_over_time"):
            return format_time_series(report, params)
        if isinstance(report, dict) and "summary" in report:
            return str(report["summary"])
        if isinstance(report, str):
            return report
        return "Report generated — see attached structured data for details."
    except Exception:
        return "Failed to format a human-friendly summary for this report."
