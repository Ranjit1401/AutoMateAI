from app.graph.workflow import graph

state = {

    "user_input": "Plan a Goa trip under ₹30000",

    "user_id": None,

    "task_type": "",

    "execution_plan": [],

    "current_agent": "",

    "agent_outputs": {},

    "final_response": ""
}

result = graph.invoke(state)

print(result)