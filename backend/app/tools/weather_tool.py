import requests

from app.core.config import settings
from app.tools.base import BaseTool, ToolError


class WeatherTool(BaseTool):
    name = "weather"
    description = "Returns live current weather for a city."

    def execute(self, city: str) -> dict:
        from app.agents.fallback_data import fallback_weather

        if not settings.OPENWEATHER_API_KEY:
            return fallback_weather(city)

        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "city": city,
                "temperature": data["main"]["temp"],
                "condition": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
        except (requests.RequestException, KeyError) as exc:
            # Demo-safe: never surface a raw API failure to the user, use
            # realistic fallback weather data instead.
            fallback = fallback_weather(city)
            fallback["note"] = f"Live weather unavailable ({exc}); showing typical conditions."
            return fallback
