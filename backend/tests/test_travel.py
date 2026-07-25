from app.agents.travel_agent import TravelAgent

agent = TravelAgent()

result = agent.extract(

"""
I want to travel from Mumbai to Goa.

Budget ₹30000

5 July to 10 July

2 people

"""

)

print(result)