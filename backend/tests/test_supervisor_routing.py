from app.agents.supervisor_agent import SupervisorAgent


def test_supervisor_routes_by_keyword():
    supervisor = SupervisorAgent()
    result = supervisor.decide(
        goal="Plan a trip",
        steps=[
            "Find restaurants near the hotel",
            "Calculate the total budget",
            "Get directions from the airport",
            "Reserve the top flight",
            "Build a day-by-day itinerary",
            "Research top attractions",
            "Check the weather forecast",
        ],
    )
    agents = [task.agent for task in result.tasks]
    assert agents == ["restaurant", "budget", "maps", "booking", "itinerary", "research", "travel"]
