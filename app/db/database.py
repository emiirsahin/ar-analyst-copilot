from pathlib import Path
import sqlite3

from app.config import settings


def _extract_sqlite_path(database_url: str) -> Path:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError(
            f"Unsupported database URL: {database_url}. Expected SQLite URL starting with '{prefix}'."
        )

    relative_path = database_url[len(prefix):]
    return Path(relative_path)


def get_db_connection() -> sqlite3.Connection:
    db_path = _extract_sqlite_path(settings.database_url)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection