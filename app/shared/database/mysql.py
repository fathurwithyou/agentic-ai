from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from app.config import settings

engine: Engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
)