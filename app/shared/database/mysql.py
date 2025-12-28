from langchain_community.utilities.sql_database import SQLDatabase

from app.config import settings

mysql_db = SQLDatabase.from_uri(settings.DATABASE_URL, engine_args={
    "pool_size": 10,
    "max_overflow": 20,
    "pool_pre_ping": True,
    "pool_recycle": 1800,
})
