from __future__ import annotations

from typing import Any

from app.services.ar_analytics import (
    get_customer_risk_summary,
    get_followup_priority_list,
    get_overdue_invoices,
)


def tool_get_overdue_invoices(region: str | None = None) -> dict[str, Any]:
    items = get_overdue_invoices()

    if region is not None:
        items = [item for item in items if item["region"].lower() == region.lower()]

    return {
        "tool_name": "get_overdue_invoices",
        "filters": {
            "region": region,
        },
        "count": len(items),
        "items": items,
    }


def tool_get_customer_risk_summary(customer_id: int) -> dict[str, Any]:
    result = get_customer_risk_summary(customer_id)

    return {
        "tool_name": "get_customer_risk_summary",
        "input": {
            "customer_id": customer_id,
        },
        "result": result,
    }


def tool_get_followup_priority_list(limit: int = 5) -> dict[str, Any]:
    if limit <= 0:
        raise ValueError("limit must be greater than 0")

    if limit > 100:
        raise ValueError("limit must be less than or equal to 100")

    items = get_followup_priority_list(limit=limit)

    return {
        "tool_name": "get_followup_priority_list",
        "input": {
            "limit": limit,
        },
        "count": len(items),
        "items": items,
    }