from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.workflow import graph
from app.memory.session_manager import session_manager

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    # Get or create session
    memory = session_manager.get_session(request.session_id)

    # Save user message
    memory.add_user_message(request.message)

    # Initial LangGraph state
    state = {
    "session_id": request.session_id,
    "user_input": request.message,
    "conversation_history": memory.get_history(),
    "user_id": None,
    "task_type": "",
    "execution_plan": [],
    "current_agent": "",
    "supervisor_tasks": [],
    "agent_outputs": {},
    "execution_log": [],   # <-- NEW
    "final_response": None,
}

    # Execute workflow
    result = graph.invoke(state)
    print("GRAPH RESULT:", result.get("execution_log"))
    print("RETURNING:", result.get("execution_log", []))

    # Save assistant response
    if result.get("final_response"):
        memory.add_assistant_message(result["final_response"])

    response = {
    "session_id": request.session_id,
    "response": result.get("final_response"),
    "execution": [],
}

    seen = set()
    execution = []

    for step in result.get("execution_log", []):
        key = (step["agent"], step["message"])
        if key not in seen:
            seen.add(key)
            execution.append(step)

    return {
        "session_id": request.session_id,
        "response": result.get("final_response"),
        "execution": execution,
    }


    print("FINAL RESPONSE:", response)

    return response