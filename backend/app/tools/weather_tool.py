import requests

from app.core.config import settings
from app.tools.base import BaseTool, ToolError


class WeatherTool(BaseTool):
    name = "weather"
    description = "Returns live current weather for a city."

    def execute(self, city: str) -> dict:
        if not settings.OPENWEATHER_API_KEY:
            raise ToolError("OPENWEATHER_API_KEY is not configured.")

        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"},
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ToolError(f"Weather lookup failed for '{city}': {exc}") from exc

        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["main"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
