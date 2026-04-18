from __future__ import annotations

import random
from datetime import date, timedelta

from app.db.database import get_db_connection
from app.db.schema import initialize_database


random.seed(42)


CUSTOMERS = [
    ("Acme Manufacturing", "EMEA", "Manufacturing", 50000.0, "medium"),
    ("BlueWave Retail", "NA", "Retail", 75000.0, "low"),
    ("Crestline Logistics", "EMEA", "Logistics", 60000.0, "medium"),
    ("Delta Industrial", "APAC", "Industrial", 90000.0, "high"),
    ("Everpeak Foods", "NA", "Food", 45000.0, "low"),
    ("Falcon Components", "EMEA", "Manufacturing", 80000.0, "high"),
    ("GreenField Health", "APAC", "Healthcare", 70000.0, "medium"),
    ("Horizon Supplies", "NA", "Wholesale", 55000.0, "medium"),
]


NOTE_TYPES = ["call", "email", "reminder", "dispute", "account_review"]
OUTCOMES = ["pending", "promised_payment", "no_response", "resolved", "escalated"]


def reset_tables() -> None:
    with get_db_connection() as connection:
        connection.execute("DELETE FROM payments")
        connection.execute("DELETE FROM interactions")
        connection.execute("DELETE FROM invoices")
        connection.execute("DELETE FROM customers")
        connection.commit()


def seed_customers() -> None:
    with get_db_connection() as connection:
        connection.executemany(
            """
            INSERT INTO customers (name, region, industry, credit_limit, risk_rating)
            VALUES (?, ?, ?, ?, ?)
            """,
            CUSTOMERS,
        )
        connection.commit()


def seed_invoices_and_payments() -> None:
    today = date.today()

    with get_db_connection() as connection:
        customer_rows = connection.execute("SELECT id FROM customers").fetchall()

        invoice_id = 1
        payment_id = 1

        for customer in customer_rows:
            customer_id = customer["id"]

            num_invoices = random.randint(5, 10)

            for _ in range(num_invoices):
                issue_offset = random.randint(15, 180)
                issue_date = today - timedelta(days=issue_offset)

                payment_terms_days = random.choice([15, 30, 45, 60])
                due_date = issue_date + timedelta(days=payment_terms_days)

                amount = round(random.uniform(1000, 20000), 2)

                is_paid = random.random() < 0.6
                dispute_flag = 1 if random.random() < 0.15 else 0

                status = "paid" if is_paid else random.choice(["open", "overdue"])

                connection.execute(
                    """
                    INSERT INTO invoices (
                        id,
                        customer_id,
                        amount,
                        issue_date,
                        due_date,
                        status,
                        payment_terms,
                        dispute_flag
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        invoice_id,
                        customer_id,
                        amount,
                        issue_date.isoformat(),
                        due_date.isoformat(),
                        status,
                        f"NET {payment_terms_days}",
                        dispute_flag,
                    ),
                )

                if is_paid:
                    payment_delay = random.randint(0, 20)
                    payment_date = due_date - timedelta(days=random.randint(0, 5))

                    if random.random() < 0.25:
                        payment_date = due_date + timedelta(days=payment_delay)

                    connection.execute(
                        """
                        INSERT INTO payments (
                            id,
                            customer_id,
                            invoice_id,
                            amount,
                            payment_date
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            payment_id,
                            customer_id,
                            invoice_id,
                            amount,
                            payment_date.isoformat(),
                        ),
                    )
                    payment_id += 1

                invoice_id += 1

        connection.commit()


def seed_interactions() -> None:
    today = date.today()

    with get_db_connection() as connection:
        customer_rows = connection.execute("SELECT id, name FROM customers").fetchall()

        interaction_id = 1

        for customer in customer_rows:
            customer_id = customer["id"]
            customer_name = customer["name"]

            num_interactions = random.randint(1, 4)

            for _ in range(num_interactions):
                days_ago = random.randint(1, 90)
                created_at = today - timedelta(days=days_ago)

                note_type = random.choice(NOTE_TYPES)
                outcome = random.choice(OUTCOMES)
                note_text = f"{note_type.title()} logged for {customer_name}."

                connection.execute(
                    """
                    INSERT INTO interactions (
                        id,
                        customer_id,
                        note_type,
                        note_text,
                        created_at,
                        outcome
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        interaction_id,
                        customer_id,
                        note_type,
                        note_text,
                        created_at.isoformat(),
                        outcome,
                    ),
                )
                interaction_id += 1

        connection.commit()


def main() -> None:
    initialize_database()
    reset_tables()
    seed_customers()
    seed_invoices_and_payments()
    seed_interactions()
    print("Database seeded successfully.")


if __name__ == "__main__":
    main()