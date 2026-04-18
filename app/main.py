from fastapi import FastAPI

from app.config import settings


app = FastAPI(
    title="AR Analyst Copilot",
    description="AI copilot for SAP-like accounts receivable analysis",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "AR Analyst Copilot API is running",
        "environment": settings.app_env,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
        "database_url": settings.database_url,
    }