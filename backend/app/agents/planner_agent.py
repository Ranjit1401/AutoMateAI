from app.agents.base_agent import BaseAgent
from app.schemas.planner import PlannerResponse


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.planner = self.llm.with_structured_output(
            PlannerResponse
        )

    def plan(self, user_input: str, task_type: str):

        prompt = f"""
You are an AI Planning Agent.

Task Type:
{task_type}

User Request:
{user_input}

Your job is to create a logical execution plan.

Rules:

1. Always return a valid PlannerResponse.

2. Use ONLY these execution steps:

- book_flight
- book_hotel
- check_weather
- plan_activities
- generate_itinerary
- estimate_budget

3. The execution order MUST ALWAYS be:

1. book_flight
2. book_hotel
3. check_weather
4. plan_activities
5. generate_itinerary
6. estimate_budget

IMPORTANT:

- Budget estimation MUST always be the LAST step because it depends on
  flights, hotels, weather and itinerary information.

- Never place estimate_budget before any travel-related task.

Example:

Goal:
Plan a 5-day trip from Mumbai to Goa.

Steps:
- book_flight
- book_hotel
- check_weather
- plan_activities
- generate_itinerary
- estimate_budget
"""

        result = self.planner.invoke(prompt)

        print("========== RAW PLANNER ==========")
        print(result)

        return result