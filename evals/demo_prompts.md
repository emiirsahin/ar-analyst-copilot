\# Demo Prompts



This file contains recommended prompts for demonstrating AR Analyst Copilot through Claude Desktop.



\## Prompt 1 — Follow-up prioritization



Which customers need immediate follow-up?



\### What this demonstrates

\- collections prioritization

\- ranked output

\- business-oriented reasoning



\### Likely tool usage

\- get\_followup\_priority\_list



\---



\## Prompt 2 — Customer risk drill-down



Give me a risk summary for customer 1.



\### What this demonstrates

\- single-customer analysis

\- deterministic risk scoring

\- explanation of risk drivers



\### Likely tool usage

\- get\_customer\_risk\_summary



\---



\## Prompt 3 — Invoice-level detail



Show overdue invoices in EMEA.



\### What this demonstrates

\- invoice-level retrieval

\- filtering by region

\- structured business data access



\### Likely tool usage

\- get\_overdue\_invoices



\---



\## Prompt 4 — Regional comparison



Which region has the highest overdue risk?



\### What this demonstrates

\- aggregate risk analysis

\- regional comparison

\- summary-level reasoning



\### Likely tool usage

\- get\_region\_risk\_summary



\---



\## Prompt 5 — Multi-tool workflow



Which region has the highest overdue risk, identify the top risky customer in that region, explain their payment behavior, and draft a follow-up email.



\### What this demonstrates

\- summary-to-detail drill-down

\- multi-tool orchestration

\- payment behavior analysis

\- action generation



\### Likely tool usage

\- get\_region\_risk\_summary

\- get\_followup\_priority\_list

\- get\_customer\_payment\_behavior

\- draft\_collection\_email

\- possibly get\_customer\_risk\_summary



\---



\## Prompt 6 — Quick evidence check



What is the overdue amount for customer 3?



\### What this demonstrates

\- grounded, data-backed answering

\- distinction between real retrieval and generic LLM text



\### Likely tool usage

\- get\_customer\_risk\_summary

\- possibly get\_overdue\_invoices

