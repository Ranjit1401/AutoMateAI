import requests

from app.core.config import settings
from app.tools.base import BaseTool


class WeatherTool(BaseTool):

    name = "weather"

    description = "Returns live weather information for a city."

    def execute(self, city: str):

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["main"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }