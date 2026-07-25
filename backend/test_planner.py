from app.agents.planner_agent import PlannerAgent

planner = PlannerAgent()

result = planner.plan(
    user_input="Plan a Goa trip under ₹30000 for 5 days",
    task_type="travel"
)

print(result)