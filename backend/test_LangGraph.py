from app.graph.workflow import graph

state = {
    "user_input": "Plan a trip from Mumbai to Goa under ₹30000",
    "user_id": None,
    "task_type": "",
    "execution_plan": [],
    "current_agent": "",
    "agent_outputs": {},
    "supervisor_tasks": [],
    "final_response": None
}

result = graph.invoke(state)

from pprint import pprint
pprint(result)