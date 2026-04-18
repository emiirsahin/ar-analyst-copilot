from __future__ import annotations

from typing import Any, Callable

from app.tools.ar_tools import (
    tool_get_customer_risk_summary,
    tool_get_followup_priority_list,
    tool_get_overdue_invoices,
)


ToolFunction = Callable[..., dict[str, Any]]


TOOL_REGISTRY: dict[str, ToolFunction] = {
    "get_overdue_invoices": tool_get_overdue_invoices,
    "get_customer_risk_summary": tool_get_customer_risk_summary,
    "get_followup_priority_list": tool_get_followup_priority_list,
}


def list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "get_overdue_invoices",
            "description": "Return overdue accounts receivable invoices, optionally filtered by region.",
            "inputs": {
                "region": {
                    "type": "string | null",
                    "required": False,
                }
            },
        },
        {
            "name": "get_customer_risk_summary",
            "description": "Return a risk summary for a single customer.",
            "inputs": {
                "customer_id": {
                    "type": "integer",
                    "required": True,
                }
            },
        },
        {
            "name": "get_followup_priority_list",
            "description": "Return a ranked list of customers who most need collections follow-up.",
            "inputs": {
                "limit": {
                    "type": "integer",
                    "required": False,
                    "default": 5,
                }
            },
        },
    ]