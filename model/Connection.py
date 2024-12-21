import sqlite3, os

from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE") or "database.db"


class DbConnection:
    _connection = None

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        cls._connection = cls._connection or sqlite3.connect(DATABASE)
        return cls._connection
