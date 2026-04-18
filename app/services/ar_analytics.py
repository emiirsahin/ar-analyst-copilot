from __future__ import annotations

from datetime import date
from typing import Any

from app.db.database import get_db_connection


def get_overdue_invoices() -> list[dict[str, Any]]:
    today = date.today().isoformat()

    query = """
    SELECT
        invoices.id AS invoice_id,
        customers.id AS customer_id,
        customers.name AS customer_name,
        customers.region AS region,
        invoices.amount AS amount,
        invoices.issue_date AS issue_date,
        invoices.due_date AS due_date,
        invoices.status AS status,
        invoices.dispute_flag AS dispute_flag,
        CAST(julianday(?) - julianday(invoices.due_date) AS INTEGER) AS days_overdue
    FROM invoices
    JOIN customers ON invoices.customer_id = customers.id
    WHERE invoices.status IN ('open', 'overdue')
      AND invoices.due_date < ?
    ORDER BY days_overdue DESC, invoices.amount DESC
    """

    with get_db_connection() as connection:
        rows = connection.execute(query, (today, today)).fetchall()

    results: list[dict[str, Any]] = []
    for row in rows:
        results.append(
            {
                "invoice_id": row["invoice_id"],
                "customer_id": row["customer_id"],
                "customer_name": row["customer_name"],
                "region": row["region"],
                "amount": row["amount"],
                "issue_date": row["issue_date"],
                "due_date": row["due_date"],
                "status": row["status"],
                "dispute_flag": bool(row["dispute_flag"]),
                "days_overdue": row["days_overdue"],
            }
        )

    return results


def get_customer_risk_summary(customer_id: int) -> dict[str, Any]:
    with get_db_connection() as connection:
        customer = connection.execute(
            """
            SELECT id, name, region, industry, credit_limit, risk_rating
            FROM customers
            WHERE id = ?
            """,
            (customer_id,),
        ).fetchone()

        if customer is None:
            raise ValueError(f"Customer with id {customer_id} was not found.")

        overdue_invoice_count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM invoices
            WHERE customer_id = ?
              AND status IN ('open', 'overdue')
              AND due_date < date('now')
            """,
            (customer_id,),
        ).fetchone()["count"]

        overdue_amount = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM invoices
            WHERE customer_id = ?
              AND status IN ('open', 'overdue')
              AND due_date < date('now')
            """,
            (customer_id,),
        ).fetchone()["total"]

        dispute_count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM invoices
            WHERE customer_id = ?
              AND dispute_flag = 1
            """,
            (customer_id,),
        ).fetchone()["count"]

        average_payment_delay = connection.execute(
            """
            SELECT COALESCE(AVG(julianday(payments.payment_date) - julianday(invoices.due_date)), 0) AS avg_delay
            FROM payments
            JOIN invoices ON payments.invoice_id = invoices.id
            WHERE payments.customer_id = ?
            """,
            (customer_id,),
        ).fetchone()["avg_delay"]

        recent_interactions = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM interactions
            WHERE customer_id = ?
              AND created_at >= date('now', '-30 day')
            """,
            (customer_id,),
        ).fetchone()["count"]

    risk_score = 0
    reasons: list[str] = []

    if overdue_invoice_count >= 3:
        risk_score += 30
        reasons.append("Multiple overdue invoices")
    elif overdue_invoice_count > 0:
        risk_score += 15
        reasons.append("Has overdue invoices")

    if overdue_amount >= 30000:
        risk_score += 30
        reasons.append("High overdue balance")
    elif overdue_amount >= 10000:
        risk_score += 15
        reasons.append("Moderate overdue balance")

    if dispute_count >= 2:
        risk_score += 20
        reasons.append("Multiple disputed invoices")
    elif dispute_count == 1:
        risk_score += 10
        reasons.append("Has a disputed invoice")

    if average_payment_delay > 10:
        risk_score += 20
        reasons.append("Pays significantly late on average")
    elif average_payment_delay > 3:
        risk_score += 10
        reasons.append("Pays somewhat late on average")

    if recent_interactions >= 3:
        risk_score += 10
        reasons.append("Frequent recent collection activity")

    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 35:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "region": customer["region"],
        "industry": customer["industry"],
        "credit_limit": customer["credit_limit"],
        "sap_risk_rating": customer["risk_rating"],
        "metrics": {
            "overdue_invoice_count": overdue_invoice_count,
            "overdue_amount": round(float(overdue_amount), 2),
            "dispute_count": dispute_count,
            "average_payment_delay_days": round(float(average_payment_delay), 2),
            "recent_interactions_30d": recent_interactions,
        },
        "calculated_risk": {
            "score": risk_score,
            "level": risk_level,
            "reasons": reasons,
        },
    }


def get_followup_priority_list(limit: int = 5) -> list[dict[str, Any]]:
    with get_db_connection() as connection:
        customers = connection.execute(
            """
            SELECT id, name, region
            FROM customers
            """
        ).fetchall()

    ranked_customers: list[dict[str, Any]] = []

    for customer in customers:
        summary = get_customer_risk_summary(customer["id"])
        ranked_customers.append(
            {
                "customer_id": summary["customer_id"],
                "customer_name": summary["customer_name"],
                "region": summary["region"],
                "risk_score": summary["calculated_risk"]["score"],
                "risk_level": summary["calculated_risk"]["level"],
                "overdue_amount": summary["metrics"]["overdue_amount"],
                "overdue_invoice_count": summary["metrics"]["overdue_invoice_count"],
                "top_reasons": summary["calculated_risk"]["reasons"][:3],
            }
        )

    ranked_customers.sort(
        key=lambda customer: (
            customer["risk_score"],
            customer["overdue_amount"],
            customer["overdue_invoice_count"],
        ),
        reverse=True,
    )

    return ranked_customers[:limit]

def get_region_risk_summary() -> list[dict[str, Any]]:
    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                customers.region AS region,
                COUNT(invoices.id) AS invoice_count,
                COALESCE(SUM(invoices.amount), 0) AS total_overdue
            FROM invoices
            JOIN customers ON invoices.customer_id = customers.id
            WHERE invoices.status IN ('open', 'overdue')
              AND invoices.due_date < date('now')
            GROUP BY customers.region
            ORDER BY total_overdue DESC
            """
        ).fetchall()

    results = []
    for row in rows:
        results.append(
            {
                "region": row["region"],
                "overdue_invoice_count": row["invoice_count"],
                "total_overdue_amount": round(float(row["total_overdue"]), 2),
            }
        )

    return results

def get_customer_payment_behavior(customer_id: int) -> dict[str, Any]:
    with get_db_connection() as connection:
        avg_delay = connection.execute(
            """
            SELECT COALESCE(AVG(julianday(payments.payment_date) - julianday(invoices.due_date)), 0)
            FROM payments
            JOIN invoices ON payments.invoice_id = invoices.id
            WHERE payments.customer_id = ?
            """,
            (customer_id,),
        ).fetchone()[0]

        late_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM payments
            JOIN invoices ON payments.invoice_id = invoices.id
            WHERE payments.customer_id = ?
              AND julianday(payments.payment_date) > julianday(invoices.due_date)
            """,
            (customer_id,),
        ).fetchone()[0]

        total_payments = connection.execute(
            """
            SELECT COUNT(*)
            FROM payments
            WHERE customer_id = ?
            """,
            (customer_id,),
        ).fetchone()[0]

    return {
        "customer_id": customer_id,
        "average_delay_days": round(float(avg_delay), 2),
        "late_payments": late_count,
        "total_payments": total_payments,
        "late_ratio": round(late_count / total_payments, 2) if total_payments else 0,
    }

def draft_collection_email(customer_id: int) -> dict[str, Any]:
    summary = get_customer_risk_summary(customer_id)

    name = summary["customer_name"]
    risk = summary["calculated_risk"]["level"]
    reasons = summary["calculated_risk"]["reasons"]

    subject = f"Follow-up on outstanding balance - {name}"

    body = f"""
Dear {name},

We hope you are doing well.

We wanted to follow up regarding your account, as we have identified some outstanding items that require attention.

Key points:
- Risk level: {risk}
- Reasons: {", ".join(reasons)}

We would appreciate your prompt attention to these matters. Please let us know if there are any issues we can help resolve.

Best regards,
Accounts Receivable Team
""".strip()

    return {
        "customer_id": customer_id,
        "subject": subject,
        "body": body,
    }