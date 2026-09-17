
from pydantic import BaseModel
#from app.models.models import ConversationModel, MessageModel


class MessageModel(BaseModel):
    role: str
    content: str

class ConversationModel(BaseModel):
    conversation_id: str
    messages: list[MessageModel]

conversations = {}

def get_conversation(conversation_id):
    return conversations.get(conversation_id)

        
def add_message(conversation_id, role, content):

    if conversation_id in conversations:
        conversation = conversations[conversation_id]

        conversation.messages.append(
            MessageModel(
                role=role,
                content=content
            )
        )
    else:
        message = MessageModel(
            role=role,
            content=content
        )

        conversation = ConversationModel(
            conversation_id=conversation_id,
            messages=[message]
        )

        conversations[conversation_id] = conversation




# 1. Conversation doesn't exist yet
conversation = get_conversation("abc")

print("Before:", conversation)


# 2. Add first user message
add_message("abc", "user", "What is RAG?")

print("After first message:")
print(get_conversation("abc"))


# 3. Add assistant message
add_message("abc", "assistant", "RAG stands for Retrieval-Augmented Generation.")

print("After assistant message:")
print(get_conversation("abc"))


# 4. Add another user message
add_message("abc", "user", "Why do we use embeddings?")

print("After second user message:")
print(get_conversation("abc"))


# 5. Check a different conversation
print("Other conversation:")
print(get_conversation("xyz"))