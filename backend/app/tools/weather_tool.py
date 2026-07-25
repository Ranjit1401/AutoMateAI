from app.tools.base_tool import BaseTool


class WeatherTool(BaseTool):

    name = "weather"

    description = "Returns weather information."

    def execute(self, city: str):

        # Mock data for now
        return {
            "city": city,
            "temperature": 31,
            "condition": "Sunny"
        }