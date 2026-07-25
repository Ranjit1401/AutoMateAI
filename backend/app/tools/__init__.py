from app.tools.tool_registry import ToolRegistry
from app.tools.weather_tool import WeatherTool

tool_registry = ToolRegistry()

tool_registry.register(WeatherTool())