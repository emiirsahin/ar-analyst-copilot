from fastapi import FastAPI, HTTPException

from app.config import settings
from app.db.database import get_db_connection
from app.services.ar_analytics import (
    get_customer_risk_summary,
    get_followup_priority_list,
    get_overdue_invoices,
)


app = FastAPI(
    title="AR Analyst Copilot",
    description="AI copilot for SAP-like accounts receivable analysis",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "AR Analyst Copilot API is running",
        "environment": settings.app_env,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
        "database_url": settings.database_url,
    }


@app.get("/db-summary")
def db_summary() -> dict[str, int]:
    with get_db_connection() as connection:
        customer_count = connection.execute(
            "SELECT COUNT(*) AS count FROM customers"
        ).fetchone()["count"]

        invoice_count = connection.execute(
            "SELECT COUNT(*) AS count FROM invoices"
        ).fetchone()["count"]

        payment_count = connection.execute(
            "SELECT COUNT(*) AS count FROM payments"
        ).fetchone()["count"]

        interaction_count = connection.execute(
            "SELECT COUNT(*) AS count FROM interactions"
        ).fetchone()["count"]

    return {
        "customers": customer_count,
        "invoices": invoice_count,
        "payments": payment_count,
        "interactions": interaction_count,
    }


@app.get("/analytics/overdue-invoices")
def overdue_invoices() -> dict[str, object]:
    results = get_overdue_invoices()
    return {
        "count": len(results),
        "items": results,
    }


@app.get("/analytics/customer-risk/{customer_id}")
def customer_risk(customer_id: int) -> dict[str, object]:
    try:
        return get_customer_risk_summary(customer_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.get("/analytics/followup-priority")
def followup_priority(limit: int = 5) -> dict[str, object]:
    results = get_followup_priority_list(limit=limit)
    return {
        "count": len(results),
        "items": results,
    }