from .embedding import *  # noqa
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.vectorstores import VectorStore


class Genesis:
    def __init__(self, db: SQLDatabase, vector_store: VectorStore):
        self.db = db
        self.vector_store = vector_store

    ...
