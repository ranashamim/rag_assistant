from datetime import datetime

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, Conversation, Message




DATABASE_URL = "sqlite:///app/data/conversations.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

#db = SessionLocal()

#conversation = db.get(Conversation, "abc")

#message = Message(
#    role="user",
#    content="What is RAG?",
#    created_at=datetime.now()
#)

#conversation.messages.append(message)

#db.commit()

#for message in conversation.messages:
#    print(f"{message.role}: {message.content}")
    
#db.close()


  