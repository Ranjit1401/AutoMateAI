from typing import Dict

from app.tools.base_tool import BaseTool
from app.tools.weather_tool import WeatherTool
from app.tools.flight_tool import FlightTool
from app.tools.hotel_tool import HotelTool


class ToolRegistry:

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())


# Global registry
tool_registry = ToolRegistry()

# Register tools
tool_registry.register(WeatherTool())
tool_registry.register(FlightTool())
tool_registry.register(HotelTool())
print("Registered tools:", tool_registry.list_tools())