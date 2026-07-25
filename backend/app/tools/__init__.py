from app.tools.registry import tool_registry
from app.tools.weather_tool import WeatherTool

tool_registry.register(WeatherTool())