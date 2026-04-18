from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.tools.ar_tools import (
    tool_get_customer_risk_summary,
    tool_get_followup_priority_list,
    tool_get_overdue_invoices,
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


if __name__ == "__main__":
    mcp.run()