from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.tools.ar_tools import (
    tool_draft_collection_email,
    tool_get_customer_payment_behavior,
    tool_get_customer_risk_summary,
    tool_get_followup_priority_list,
    tool_get_overdue_invoices,
    tool_get_region_risk_summary,
)


mcp = FastMCP("AR Analyst Copilot MCP Server")


@mcp.tool()
def get_overdue_invoices(region: str | None = None) -> dict:
    """
    Use this tool when you need a list of overdue accounts receivable invoices.

    Use this tool FIRST when the user asks for invoice-level data or filtering (e.g., by region).
    Prefer this over summary tools when specific invoice records are requested.

    This tool is useful for:
    - finding overdue invoices overall
    - filtering overdue invoices by region
    - checking specific overdue amounts and invoice-level details

    Returns structured invoice records including:
    - invoice id
    - customer id
    - customer name
    - region
    - amount
    - due date
    - days overdue
    - dispute flag

    If you need a customer-level risk explanation, use get_customer_risk_summary.
    If you need a regional summary instead of invoice-level detail, use get_region_risk_summary.
    """
    return tool_get_overdue_invoices(region=region)


@mcp.tool()
def get_customer_risk_summary(customer_id: int) -> dict:
    """
    Use this tool when you need a detailed risk assessment for one specific customer.

    This tool is useful for:
    - explaining why a customer is risky
    - reviewing overdue exposure for one customer
    - checking whether disputes, payment delays, and recent interactions contribute to risk

    Returns:
    - customer identity and profile fields
    - overdue invoice count
    - overdue amount
    - dispute count
    - average payment delay
    - recent interaction count
    - calculated risk score
    - calculated risk level
    - human-readable reasons for the risk assessment

    Use this after identifying a customer of interest through get_followup_priority_list
    or get_region_risk_summary.

    Do not use this to compare many customers at once.
    """
    return tool_get_customer_risk_summary(customer_id=customer_id)


@mcp.tool()
def get_followup_priority_list(limit: int = 5) -> dict:
    """
    Use this tool to identify which customers most urgently need collections follow-up.

    Prefer this tool over get_customer_risk_summary when selecting multiple customers.

    This tool is useful for:
    - ranking customers by urgency
    - deciding who should be contacted first
    - finding high-priority customers before drilling into details

    Returns a ranked list of customers with:
    - customer id
    - customer name
    - region
    - calculated risk score
    - calculated risk level
    - overdue amount
    - overdue invoice count
    - top reasons for prioritization

    Use this as a starting point when the user asks:
    - who needs immediate attention
    - who should collections contact first
    - which customers are highest priority

    After this tool, use get_customer_risk_summary for detail or
    draft_collection_email to generate an action.
    """
    return tool_get_followup_priority_list(limit=limit)


@mcp.tool()
def get_region_risk_summary() -> dict:
    """
    Use this tool when the user asks for a regional or aggregate view of overdue risk.
    
    Do NOT use this tool if the user is asking for invoice-level details or filtering.
    Use get_overdue_invoices instead for detailed invoice data.

    This tool is useful for:
    - comparing regions
    - identifying which region has the greatest overdue exposure
    - starting a drill-down workflow from summary to customer detail

    Returns a list of region summaries with:
    - region
    - overdue invoice count
    - total overdue amount

    Use this before get_followup_priority_list or get_customer_risk_summary
    when the user begins with a regional question.

    This is a summary tool, not a detailed customer tool.
    """
    return tool_get_region_risk_summary()


@mcp.tool()
def get_customer_payment_behavior(customer_id: int) -> dict:
    """
    Use this tool when you need to explain how a customer tends to pay invoices.

    This tool is useful for:
    - explaining whether a customer regularly pays late
    - supporting a risk explanation with payment behavior evidence
    - checking whether poor payment discipline is driving collections concern

    Returns:
    - customer id
    - average payment delay in days
    - number of late payments
    - total payments
    - late payment ratio

    Use this after selecting a specific customer, typically from
    get_followup_priority_list or get_customer_risk_summary.

    Do not use this for region-wide comparisons.
    """
    return tool_get_customer_payment_behavior(customer_id)


@mcp.tool()
def draft_collection_email(customer_id: int) -> dict:
    """
    Use this tool when the user wants an action-oriented follow-up for a specific customer.

    This tool is useful for:
    - drafting a collections email
    - preparing a follow-up message after analyzing a risky customer
    - turning analysis into a concrete next step

    Returns:
    - customer id
    - email subject
    - email body

    This tool should usually be used after identifying a customer through
    get_followup_priority_list, get_customer_risk_summary, or
    get_customer_payment_behavior.

    Use this tool for drafting, not for sending.
    """
    return tool_draft_collection_email(customer_id)


if __name__ == "__main__":
    mcp.run()