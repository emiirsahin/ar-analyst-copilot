# AR Analyst Copilot

A Python-based AI copilot for analyzing SAP-like accounts receivable data through structured tools exposed via an MCP-style interface.

## Goals
- Simulate enterprise finance analysis workflows  
- Expose business-safe tools to an LLM  
- Demonstrate MCP-style tool access for AI systems  
- Produce grounded, auditable answers over structured data  

## Planned stack
- Python  
- FastAPI  
- SQLite  
- Pydantic  
- MCP server  
- Claude-compatible tool use  

## Project status
Scaffolding in progress.

## Local development

### Activate virtual environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Run the API
```powershell
uvicorn app.main:app --reload
```

### Seed the database
```powershell
python -m scripts.seed_data
```
