import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from .agents.endpoints import router as agents_router
from .config import settings

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Starting the FastAPI application")

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
)

os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
os.environ["GOOGLE_CSE_ID"] = settings.GOOGLE_CSE_ID

# app.add_middleware()

app.include_router(agents_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
