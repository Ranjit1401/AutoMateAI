from app.agents.base_agent import BaseAgent
from app.schemas.planner import PlannerResponse  # <-- REQUIRED IMPORT


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
    
    Your job is to break the user's request into logical execution steps.
    
    Rules:
    
    - Flight booking -> use step: book_flight
    - Hotel booking -> use step: book_hotel
    - Weather lookup -> use step: check_weather
    - Tourist attractions -> use step: plan_activities
    - Daily trip planning -> use step: generate_itinerary
    - Cost estimation -> use step: estimate_budget
    
    Return a valid PlannerResponse.
    """
    
        result = self.planner.invoke(prompt)
    
        print("========== RAW PLANNER ==========")
        print(result)
    
        return result