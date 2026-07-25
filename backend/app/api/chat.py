from fastapi import APIRouter

from app.graph.workflow import graph

from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    state = {

        "user_input": request.message,

        "user_id": None,

        "task_type": "",

        "execution_plan": [],

        "current_agent": "",

        "agent_outputs": {},

        "final_response": ""
    }

    result = graph.invoke(state)

    return result