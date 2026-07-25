from app.executor.agent_executor import agent_executor

state = {
    "agent_outputs": {}
}

task = {
    "agent": "travel",
    "action": "Plan a trip from Mumbai to Goa under ₹30000"
}

result = agent_executor.execute(task, state)

print(result)