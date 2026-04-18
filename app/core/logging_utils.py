from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "tool_calls.jsonl"


def _utc_timestamp() -> str:
    return datetime.now(UTC).isoformat()


def log_tool_event(
    *,
    tool_name: str,
    status: str,
    input_data: dict[str, Any] | None = None,
    output_summary: dict[str, Any] | None = None,
    error_message: str | None = None,
) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": _utc_timestamp(),
        "tool_name": tool_name,
        "status": status,
        "input": input_data or {},
        "output_summary": output_summary or {},
        "error_message": error_message,
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")