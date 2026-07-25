from app.core.agent_registry import registry
from app.executor.agent_executor import agent_executor

planner_output = {
    "goal": "Plan Goa Trip",
    "steps": [
        "Plan a trip from Mumbai to Goa under ₹30000"
    ]
}

supervisor = registry.supervisor

tasks = supervisor.decide(
    goal=planner_output["goal"],
    steps=planner_output["steps"]
)

print("Supervisor Tasks:")
print(tasks.model_dump())

state = {
    "agent_outputs": {}
}

for task in tasks.tasks:
    result = agent_executor.execute(
        task.model_dump(),
        state
    )
    print(result)