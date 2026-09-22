from datetime import datetime

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, Conversation, Message




DATABASE_URL = "sqlite:///app/data/conversations.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
