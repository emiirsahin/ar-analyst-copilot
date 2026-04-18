\# Architecture



\## High-level flow



User -> Chat Client -> LLM -> Tools / MCP Server -> Analytics Layer -> SQLite DB



\## Main idea

The LLM does not access raw enterprise data directly. It calls structured tools that return controlled, auditable business information.



\## Planned modules

\- Data layer

\- Analytics services

\- MCP tool layer

\- LLM client

\- UI

