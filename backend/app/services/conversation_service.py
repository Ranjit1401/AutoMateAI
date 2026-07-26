"""DB-backed conversation/session storage. Replaces the old process-RAM
SessionManager + ConversationMemory, which lost all history on restart and
couldn't be scoped to a specific user."""
from sqlalchemy.orm import Session

from app.db.models import Conversation, Message


def get_or_create_conversation(db: Session, user_id: str, conversation_id: str | None) -> Conversation:
    if conversation_id:
        conversation = db.get(Conversation, conversation_id)
        if conversation and conversation.user_id == user_id:
            return conversation

    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.flush()
    return conversation


def add_message(db: Session, conversation_id: str, role: str, content: str, agent_trace: dict | None = None) -> Message:
    message = Message(conversation_id=conversation_id, role=role, content=content, agent_trace=agent_trace)
    db.add(message)
    db.flush()
    return message


def get_history(db: Session, conversation_id: str) -> list[dict[str, str]]:
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        return []
    return [{"role": m.role, "content": m.content} for m in conversation.messages]


def set_title_from_first_message(db: Session, conversation: Conversation, message: str) -> None:
    if conversation.title == "New conversation":
        conversation.title = (message[:60] + "…") if len(message) > 60 else message
