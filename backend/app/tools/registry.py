from app.tools.weather_tool import WeatherTool
from app.tools.flight_tool import FlightTool
from app.tools.hotel_tool import HotelTool


class ToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(self, tool):
        self._tools[tool.name] = tool

    def get(self, name: str):
        return self._tools.get(name)

    def list_tools(self):
        return list(self._tools.keys())


tool_registry = ToolRegistry()

# Register all tools
tool_registry.register(WeatherTool())
tool_registry.register(FlightTool())
tool_registry.register(HotelTool())

print("Registered tools:", tool_registry.list_tools())