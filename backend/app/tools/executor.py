from app.tools.registry import tool_registry


class ToolExecutor:

    def execute(self, tool_name: str, **kwargs):

        tool = tool_registry.get(tool_name)

        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        return tool.execute(**kwargs)


tool_executor = ToolExecutor()