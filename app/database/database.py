from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.database.models import Base


DATABASE_URL = "sqlite:///app/data/conversations.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "timeout": 30,
        "check_same_thread": False
    }
)


@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=30000")

    cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


Base.metadata.create_all(engine)