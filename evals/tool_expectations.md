\# Tool Expectations



This file documents the intended behavior of the current MCP tools and what a good Claude response should contain.



\## get\_overdue\_invoices



\### Purpose

Return overdue invoice records, optionally filtered by region.



\### Good response characteristics

\- includes invoice/customer details

\- includes overdue amount

\- includes days overdue

\- stays invoice-level rather than switching to risk scoring unless needed



\### Best use cases

\- "Show overdue invoices"

\- "Show overdue invoices in EMEA"

\- "List overdue AR items"



\---



\## get\_customer\_risk\_summary



\### Purpose

Return a detailed risk summary for one specific customer.



\### Good response characteristics

\- includes customer identity

\- includes risk score and level

\- explains reasons for risk

\- references overdue balance, disputes, and payment behavior indicators



\### Best use cases

\- "Give me a risk summary for customer 1"

\- "Why is this customer risky?"

\- "Explain this customer's overdue exposure"



\---



\## get\_followup\_priority\_list



\### Purpose

Return a ranked list of customers who most urgently need collections attention.



\### Good response characteristics

\- ranked output

\- names the highest-priority customers

\- references risk level and overdue exposure

\- helps identify who to inspect next



\### Best use cases

\- "Which customers need immediate follow-up?"

\- "Who should collections contact first?"

\- "Which accounts are highest priority?"



\---



\## get\_region\_risk\_summary



\### Purpose

Return aggregate overdue exposure by region.



\### Good response characteristics

\- compares regions

\- names the highest-risk region clearly

\- includes invoice counts and/or overdue amounts

\- stays aggregate rather than customer-specific unless asked



\### Best use cases

\- "Which region has the highest overdue risk?"

\- "Compare overdue risk by region"

\- "Where is overdue exposure concentrated?"



\---



\## get\_customer\_payment\_behavior



\### Purpose

Explain how a customer tends to pay invoices.



\### Good response characteristics

\- includes average delay

\- includes late payment count

\- includes late ratio

\- connects payment behavior to collections concern



\### Best use cases

\- "Explain this customer's payment behavior"

\- "Does this customer usually pay late?"

\- "How disciplined is this customer's payment history?"



\---



\## draft\_collection\_email



\### Purpose

Generate a draft follow-up email for a customer.



\### Good response characteristics

\- includes a usable subject line

\- includes a professional email body

\- reflects the customer's risk context

\- is clearly a draft, not a sent message



\### Best use cases

\- "Draft a follow-up email"

\- "Prepare a collections email for this customer"

\- "Write a payment follow-up note"



\---



\## Multi-tool workflow expectation



For a complex request like:



"Which region has the highest overdue risk, identify the top risky customer in that region, explain their payment behavior, and draft a follow-up email."



A good tool chain is:



1\. get\_region\_risk\_summary

2\. get\_followup\_priority\_list

3\. get\_customer\_payment\_behavior

4\. draft\_collection\_email



Possible additional tool:

\- get\_customer\_risk\_summary



A good final answer should:

\- identify the region

\- identify the customer

\- explain the customer’s payment behavior with evidence

\- provide the email draft

