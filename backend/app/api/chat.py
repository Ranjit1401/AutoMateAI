from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.graph.workflow import graph

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    result = graph.invoke({

        "user_input": request.message,

        "task_type": "",

        "execution_plan": [],

        "current_agent": "",

        "final_response": ""

    })

    return result