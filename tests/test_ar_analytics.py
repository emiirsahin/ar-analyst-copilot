from app.services.ar_analytics import (
    get_customer_risk_summary,
    get_followup_priority_list,
    get_overdue_invoices,
)


def test_get_overdue_invoices_returns_list() -> None:
    results = get_overdue_invoices()

    assert isinstance(results, list)

    if results:
        first = results[0]
        assert "invoice_id" in first
        assert "customer_name" in first
        assert "days_overdue" in first


def test_get_customer_risk_summary_returns_expected_shape() -> None:
    result = get_customer_risk_summary(1)

    assert result["customer_id"] == 1
    assert "customer_name" in result
    assert "metrics" in result
    assert "calculated_risk" in result
    assert "score" in result["calculated_risk"]
    assert "level" in result["calculated_risk"]


def test_get_followup_priority_list_respects_limit() -> None:
    results = get_followup_priority_list(limit=3)

    assert isinstance(results, list)
    assert len(results) == 3

    for item in results:
        assert "customer_id" in item
        assert "risk_score" in item
        assert "risk_level" in item