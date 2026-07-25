from typing import Any

from app.tools import tool_registry


class ToolExecutor:

    def execute(
        self,
        tool_name: str,
        **kwargs
    ) -> Any:

        tool = tool_registry.get(tool_name)

        if tool is None:
            raise Exception(
                f"Tool '{tool_name}' not found."
            )

        return tool.execute(**kwargs)


tool_executor = ToolExecutor()