from typing import Dict
from app.tools.base_tool import BaseTool


class ToolRegistry:

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())