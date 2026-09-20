
from datetime import datetime

from app.database.database import SessionLocal
from app.database.models import Conversation, Message

from sqlalchemy.orm import selectinload

from sqlalchemy import select


def get_conversation(conversation_id):

    db = SessionLocal()

    stmt = (
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.conversation_id == conversation_id)
    )

    result = db.execute(stmt)
    conversation = result.scalar_one_or_none()

    db.close()

    return conversation



        
def add_message(conversation_id, role, content):
    db = SessionLocal()
    conversation = db.get(Conversation, conversation_id)

    if conversation:
        
        message = Message(
            role=role,
            content=content,
            created_at=datetime.now()
        )
        conversation.messages.append(message)
    else:
        message = Message(
            role=role,
            content=content,
            created_at=datetime.now()
        )

        conversation = Conversation(
            conversation_id=conversation_id,
            created_at=datetime.now()
        )

        conversation.messages.append(message)
        db.add(conversation)
    db.commit()
    db.close()
        

