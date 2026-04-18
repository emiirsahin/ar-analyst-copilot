from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.tools.ar_tools import (
    tool_get_customer_risk_summary,
    tool_get_followup_priority_list,
    tool_get_overdue_invoices,
    tool_get_region_risk_summary,
    tool_get_customer_payment_behavior,
    tool_draft_collection_email,
)


mcp = FastMCP("AR Analyst Copilot MCP Server")


@mcp.tool()
def get_overdue_invoices(region: str | None = None) -> dict:
    """
    Return overdue accounts receivable invoices, optionally filtered by region.
    """
    return tool_get_overdue_invoices(region=region)


@mcp.tool()
def get_customer_risk_summary(customer_id: int) -> dict:
    """
    Return a risk summary for a single customer.
    """
    return tool_get_customer_risk_summary(customer_id=customer_id)


@mcp.tool()
def get_followup_priority_list(limit: int = 5) -> dict:
    """
    Return a ranked list of customers who most need collections follow-up.
    """
    return tool_get_followup_priority_list(limit=limit)


@mcp.tool()
def get_region_risk_summary() -> dict:
    """Return aggregated overdue risk metrics by region."""
    return tool_get_region_risk_summary()



@mcp.tool()
def get_customer_payment_behavior(customer_id: int) -> dict:
    """Analyze how a customer pays invoices (delays, ratios)."""
    return tool_get_customer_payment_behavior(customer_id)



@mcp.tool()
def draft_collection_email(customer_id: int) -> dict:
    """Generate a draft follow-up email for a customer."""
    return tool_draft_collection_email(customer_id)


if __name__ == "__main__":
    mcp.run()