# AR Analyst Copilot

A Python-based AI copilot for analyzing SAP-like accounts receivable data through structured tools exposed via an MCP server.

## Project overview

This project simulates an enterprise finance assistant that works over SAP-like accounts receivable data.

It uses:
- deterministic analytics written in Python
- tool wrappers that expose business-safe capabilities
- an MCP server that makes those tools available to AI clients
- Claude Desktop as a local MCP host for natural language interaction
- SQLite as the local data store

The goal is to demonstrate a practical enterprise AI architecture where an LLM does not directly access raw business data. Instead, it uses approved tools that encapsulate business logic and return structured outputs.

## Current capabilities

The system currently supports:
- overdue invoice analysis
- customer risk summaries
- collections follow-up prioritization
- region-level overdue risk summaries
- customer payment behavior analysis
- draft collection email generation

Tool calls are logged to a local JSONL log for observability and debugging.

## Architecture

High-level flow:

User -> Claude Desktop -> Local MCP Server -> Tool Wrappers -> Analytics Layer -> SQLite Database

Developer/debug flow:

Developer -> FastAPI Endpoints -> Analytics Layer / Tool Wrappers -> SQLite Database

## Repository structure

```text
ar-analyst-copilot/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── core/
│   │   └── logging_utils.py
│   ├── db/
│   │   ├── database.py
│   │   └── schema.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── server.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── ar_analytics.py
│   └── tools/
│       ├── __init__.py
│       ├── ar_tools.py
│       └── registry.py
├── docs/
│   └── architecture.md
├── evals/
├── logs/
├── prompts/
├── scripts/
│   ├── __init__.py
│   ├── run_mcp_server.py
│   ├── seed_data.py
│   └── test_mcp_client.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Local setup

### 1. Create and activate the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

Copy the template file:

```powershell
Copy-Item .env.example .env
```

Then fill in your local values.

Example:

```env
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-6
APP_ENV=development
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///E:/ar-analyst-copilot/ar_analyst.db
```

### Important note for Windows + Claude Desktop

Use an absolute SQLite path in `DATABASE_URL`.

Relative SQLite paths may work when running directly from a terminal, but can fail or point to the wrong file when the MCP server is launched by Claude Desktop.

Recommended format:

```env
DATABASE_URL=sqlite:///E:/ar-analyst-copilot/ar_analyst.db
```

## Database setup

### Seed the database

Default deterministic seed:

```powershell
python -m scripts.seed_data
```

Custom seed:

```powershell
python -m scripts.seed_data --seed 123
```

The seed script creates:
- customers
- invoices
- payments
- interactions

By default, the script uses a fixed random seed for reproducibility.

## Running the FastAPI app

```powershell
uvicorn app.main:app --reload
```

Useful endpoints:
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/db-summary`
- `http://127.0.0.1:8000/analytics/overdue-invoices`
- `http://127.0.0.1:8000/analytics/customer-risk/1`
- `http://127.0.0.1:8000/analytics/followup-priority`
- `http://127.0.0.1:8000/tools`

## Running the MCP server directly

You can launch the MCP server manually with:

```powershell
python -m app.mcp.server
```

Or through the helper runner script used by Claude Desktop:

```powershell
E:\ar-analyst-copilot\.venv\Scripts\python.exe E:\ar-analyst-copilot\scripts\run_mcp_server.py
```

## Claude Desktop integration

Claude Desktop can connect to the local MCP server over stdio.

Example Claude Desktop config on Windows:

```json
{
  "mcpServers": {
    "ar-analyst-copilot": {
      "command": "E:\\ar-analyst-copilot\\.venv\\Scripts\\python.exe",
      "args": ["E:\\ar-analyst-copilot\\scripts\\run_mcp_server.py"],
      "cwd": "E:\\ar-analyst-copilot"
    }
  }
}
```

Your actual config file lives at:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

After changing the config:
- fully close Claude Desktop
- reopen it
- start a new chat

## Example prompts for Claude Desktop

Basic prompts:
- Which customers need immediate follow-up?
- Give me a risk summary for customer 1.
- Show overdue invoices in EMEA.
- What is the overdue amount for customer 3?

Multi-tool demo prompt:
- Which region has the highest overdue risk, identify the top risky customer in that region, explain their payment behavior, and draft a follow-up email.

## Logging

Tool calls are logged to:

```text
logs/tool_calls.jsonl
```

Each log entry includes:
- timestamp
- tool name
- status
- input arguments
- output summary
- error message if applicable

This helps inspect multi-tool execution order and debug Claude behavior.

## Why both FastAPI endpoints and MCP?

The FastAPI app is useful for:
- direct debugging
- inspecting analytics outputs
- validating tool wrapper responses without involving Claude
- serving as a future backend for a custom UI

The MCP server is useful for:
- exposing tools to AI hosts in a standard format
- connecting Claude Desktop to the business logic
- demonstrating enterprise AI integration patterns