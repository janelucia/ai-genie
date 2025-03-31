from langchain.memory import ConversationBufferMemory
from ..models import Message, Chat

def create_memory(chat_id) -> ConversationBufferMemory:
    """
    Creates a chat-specific memory instance by loading previous messages.
    """
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return None

    # Retrieve previous messages for the chat
    previous_messages = Message.objects.filter(chat=chat).order_by("created")
    
    # Initialize memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Populate memory with previous messages
    for msg in previous_messages:
        if msg.ai_response:
            memory.chat_memory.add_ai_message(msg.content)
        else:
            memory.chat_memory.add_user_message(msg.content)

    return memory