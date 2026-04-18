from __future__ import annotations

from typing import Any

from app.core.logging_utils import log_tool_event
from app.services.ar_analytics import (
    get_customer_risk_summary,
    get_followup_priority_list,
    get_overdue_invoices,
    get_region_risk_summary,
    get_customer_payment_behavior,
    draft_collection_email,
)

def tool_get_overdue_invoices(region: str | None = None) -> dict[str, Any]:
    tool_name = "get_overdue_invoices"
    input_data = {"region": region}

    try:
        items = get_overdue_invoices()

        if region is not None:
            items = [item for item in items if item["region"].lower() == region.lower()]

        result = {
            "tool_name": tool_name,
            "filters": {
                "region": region,
            },
            "count": len(items),
            "items": items,
        }

        log_tool_event(
            tool_name=tool_name,
            status="success",
            input_data=input_data,
            output_summary={"count": len(items)},
        )

        return result

    except Exception as error:
        log_tool_event(
            tool_name=tool_name,
            status="error",
            input_data=input_data,
            error_message=str(error),
        )
        raise


def tool_get_customer_risk_summary(customer_id: int) -> dict[str, Any]:
    tool_name = "get_customer_risk_summary"
    input_data = {"customer_id": customer_id}

    try:
        result_data = get_customer_risk_summary(customer_id)

        result = {
            "tool_name": tool_name,
            "input": {
                "customer_id": customer_id,
            },
            "result": result_data,
        }

        log_tool_event(
            tool_name=tool_name,
            status="success",
            input_data=input_data,
            output_summary={
                "customer_name": result_data["customer_name"],
                "risk_level": result_data["calculated_risk"]["level"],
                "risk_score": result_data["calculated_risk"]["score"],
            },
        )

        return result

    except Exception as error:
        log_tool_event(
            tool_name=tool_name,
            status="error",
            input_data=input_data,
            error_message=str(error),
        )
        raise


def tool_get_followup_priority_list(limit: int = 5) -> dict[str, Any]:
    tool_name = "get_followup_priority_list"
    input_data = {"limit": limit}

    try:
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

        if limit > 100:
            raise ValueError("limit must be less than or equal to 100")

        items = get_followup_priority_list(limit=limit)

        result = {
            "tool_name": tool_name,
            "input": {
                "limit": limit,
            },
            "count": len(items),
            "items": items,
        }

        log_tool_event(
            tool_name=tool_name,
            status="success",
            input_data=input_data,
            output_summary={"count": len(items)},
        )

        return result

    except Exception as error:
        log_tool_event(
            tool_name=tool_name,
            status="error",
            input_data=input_data,
            error_message=str(error),
        )
        raise

def tool_get_region_risk_summary() -> dict[str, Any]:
    tool_name = "get_region_risk_summary"

    try:
        items = get_region_risk_summary()

        result = {
            "tool_name": tool_name,
            "count": len(items),
            "items": items,
        }

        log_tool_event(
            tool_name=tool_name,
            status="success",
            output_summary={"count": len(items)},
        )

        return result

    except Exception as error:
        log_tool_event(
            tool_name=tool_name,
            status="error",
            error_message=str(error),
        )
        raise

def tool_get_customer_payment_behavior(customer_id: int) -> dict[str, Any]:
    tool_name = "get_customer_payment_behavior"
    input_data = {"customer_id": customer_id}

    try:
        result_data = get_customer_payment_behavior(customer_id)

        result = {
            "tool_name": tool_name,
            "input": input_data,
            "result": result_data,
        }

        log_tool_event(
            tool_name=tool_name,
            status="success",
            input_data=input_data,
            output_summary={
                "avg_delay": result_data["average_delay_days"]
            },
        )

        return result

    except Exception as error:
        log_tool_event(
            tool_name=tool_name,
            status="error",
            input_data=input_data,
            error_message=str(error),
        )
        raise

def tool_draft_collection_email(customer_id: int) -> dict[str, Any]:
    tool_name = "draft_collection_email"
    input_data = {"customer_id": customer_id}

    try:
        result_data = draft_collection_email(customer_id)

        result = {
            "tool_name": tool_name,
            "input": input_data,
            "result": result_data,
        }

        log_tool_event(
            tool_name=tool_name,
            status="success",
            input_data=input_data,
        )

        return result

    except Exception as error:
        log_tool_event(
            tool_name=tool_name,
            status="error",
            input_data=input_data,
            error_message=str(error),
        )
        raise