from app.agents.supervisor_agent import SupervisorAgent

supervisor = SupervisorAgent()

result = supervisor.decide(
    goal="Plan Goa Trip",
    steps=[
        "Research destination",
        "Find flights",
        "Find hotels",
        "Estimate expenses"
    ]
)

print(result.model_dump())