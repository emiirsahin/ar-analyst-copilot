import pytest

from app.tools.ar_tools import (
    tool_get_customer_risk_summary,
    tool_get_followup_priority_list,
    tool_get_overdue_invoices,
)


def test_tool_get_overdue_invoices_returns_expected_shape() -> None:
    result = tool_get_overdue_invoices()

    assert result["tool_name"] == "get_overdue_invoices"
    assert "count" in result
    assert "items" in result
    assert isinstance(result["items"], list)


def test_tool_get_customer_risk_summary_returns_expected_shape() -> None:
    result = tool_get_customer_risk_summary(1)

    assert result["tool_name"] == "get_customer_risk_summary"
    assert result["input"]["customer_id"] == 1
    assert "result" in result
    assert result["result"]["customer_id"] == 1


def test_tool_get_followup_priority_list_rejects_invalid_limit() -> None:
    with pytest.raises(ValueError):
        tool_get_followup_priority_list(limit=0)