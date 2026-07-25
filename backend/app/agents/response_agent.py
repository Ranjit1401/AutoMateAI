from app.agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):

    def generate(self, state):

        execution = state["agent_outputs"]["execution"]

        if not execution:
            return "No results were generated."

        travel = execution[0]["result"]["travel"]
        weather = execution[0]["result"]["weather"]

        lines = []

        lines.append("✅ Your travel plan is ready!\n")

        lines.append(f"📍 From: {travel['source']}")
        lines.append(f"🏝 Destination: {travel['destination']}")
        lines.append(f"💰 Budget: ₹{travel['budget']}")
        lines.append(f"👥 Travellers: {travel['travellers']}")

        lines.append("")

        lines.append("🌦 Current Weather")

        lines.append(
            f"{weather['condition']}, "
            f"{weather['temperature']}°C"
        )

        lines.append(
            f"Humidity: {weather['humidity']}%"
        )

        lines.append(
            f"Wind Speed: {weather['wind_speed']} m/s"
        )

        lines.append("")

        lines.append("📋 Planned Tasks")

        for item in execution:
            lines.append(f"• {item['task']['action']}")

        return "\n".join(lines)