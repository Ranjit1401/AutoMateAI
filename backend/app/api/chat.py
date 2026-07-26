import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.agent_registry import registry
from app.core.logging_config import get_logger
from app.db.models import Conversation, User
from app.graph.workflow import graph
from app.schemas.chat import ChatRequest, ChatResponse, ConversationDetailOut, ConversationOut
from app.services import conversation_service, log_service, memory_service, task_service

router = APIRouter(tags=["Chat"])
logger = get_logger(__name__)


def _build_initial_state(db: Session, user: User, conversation: Conversation, message: str) -> dict:
    conversation_service.add_message(db, conversation.id, "user", message)
    conversation_service.set_title_from_first_message(db, conversation, message)

    return {
        "session_id": conversation.id,
        "user_input": message,
        "conversation_history": conversation_service.get_history(db, conversation.id),
        "long_term_memory": memory_service.recent_memory_strings(db, user.id),
        "user_id": user.id,
        "task_type": "",
        "execution_plan": [],
        "current_agent": "",
        "supervisor_tasks": [],
        "agent_outputs": {},
        "final_response": None,
    }


def _persist_turn_outcome(db: Session, user: User, conversation: Conversation, message: str, result: dict) -> None:
    response_text = result.get("final_response") or "I couldn't generate a response for that."
    conversation_service.add_message(
        db, conversation.id, "assistant", response_text, agent_trace=result.get("agent_outputs")
    )

    for item in result.get("agent_outputs", {}).get("execution", []):
        task = task_service.create_task(
            db, user.id, title=item["task"]["action"], agent=item["task"]["agent"],
            action=item["task"]["action"], conversation_id=conversation.id,
        )
        if item["result"].get("error"):
            task_service.mark_failed(db, task, item["result"]["error"])
        else:
            task_service.mark_done(db, task, item["result"])

    try:
        memory_agent = registry.get("memory")
        extraction = memory_agent.extract(message)
        if extraction.has_durable_fact and extraction.fact:
            memory_service.add_memory(db, user.id, extraction.fact, extraction.category, conversation.id)
    except Exception:  # noqa: BLE001 — memory extraction is best-effort
        logger.exception("Memory extraction failed; continuing without it.")

    log_service.add_log(db, f"Chat turn completed for conversation {conversation.id}", source="chat", user_id=user.id)
    db.commit()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = conversation_service.get_or_create_conversation(db, user.id, payload.conversation_id)
    state = _build_initial_state(db, user, conversation, payload.message)

    try:
        result = graph.invoke(state)
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        logger.exception("Chat pipeline failed")
        raise HTTPException(status_code=500, detail=f"Agent pipeline failed: {exc}") from exc

    _persist_turn_outcome(db, user, conversation, payload.message, result)

    return ChatResponse(conversation_id=conversation.id, response=result.get("final_response") or "")


@router.post("/chat/stream")
def chat_stream(payload: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Streams pipeline progress (router -> planner -> supervisor ->
    per-agent execution -> response) as Server-Sent Events, so the frontend
    can show live status instead of a single blocking spinner. This graph
    doesn't do token-by-token LLM streaming (several steps use structured
    output, which isn't streamable token-by-token) — this streams real
    node-completion progress instead, which is what LangGraph's `.stream()`
    actually gives us."""
    conversation = conversation_service.get_or_create_conversation(db, user.id, payload.conversation_id)
    state = _build_initial_state(db, user, conversation, payload.message)

    def event_stream():
        yield f"event: start\ndata: {json.dumps({'conversation_id': conversation.id})}\n\n"

        final_state = dict(state)
        try:
            for step_output in graph.stream(state):
                node_name = next(iter(step_output))
                final_state.update(step_output[node_name])
                yield f"event: progress\ndata: {json.dumps({'node': node_name})}\n\n"
        except Exception as exc:  # noqa: BLE001
            db.rollback()
            logger.exception("Streaming chat pipeline failed")
            yield f"event: error\ndata: {json.dumps({'detail': str(exc)})}\n\n"
            return

        _persist_turn_outcome(db, user, conversation, payload.message, final_state)
        yield f"event: done\ndata: {json.dumps({'response': final_state.get('final_response') or ''})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/chat/conversations", response_model=list[ConversationOut])
def list_conversations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return sorted(user.conversations, key=lambda c: c.updated_at, reverse=True)


@router.get("/chat/conversations/{conversation_id}", response_model=ConversationDetailOut)
def get_conversation(conversation_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.get(Conversation, conversation_id)
    if conversation is None or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
