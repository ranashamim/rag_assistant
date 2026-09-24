from datetime import datetime

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from app.database.models import Base



DATABASE_URL = "sqlite:///app/data/conversations.db"

engine = create_engine(DATABASE_URL)

#SessionLocal = sessionmaker(bind=engine)
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

Base.metadata.create_all(engine)




