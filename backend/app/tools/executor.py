"""Executes a registered tool by name, with consistent logging and error
handling so a single tool failure surfaces as data, not a stack trace."""
from app.core.logging_config import get_logger
from app.tools.base import ToolError
from app.tools.registry import tool_registry

logger = get_logger(__name__)


class ToolExecutionError(Exception):
    def __init__(self, tool_name: str, message: str):
        self.tool_name = tool_name
        self.message = message
        super().__init__(f"[{tool_name}] {message}")


class ToolExecutor:
    def execute(self, tool_name: str, **kwargs):
        tool = tool_registry.get(tool_name)

        if tool is None:
            raise ToolExecutionError(tool_name, f"Unknown tool: {tool_name}")

        try:
            return tool.execute(**kwargs)
        except ToolError as exc:
            logger.warning("Tool '%s' reported a handled error: %s", tool_name, exc)
            raise ToolExecutionError(tool_name, str(exc)) from exc
        except Exception as exc:  # noqa: BLE001 — intentionally broad: any
            # unexpected failure inside a tool must not crash the whole graph.
            logger.exception("Tool '%s' failed unexpectedly", tool_name)
            raise ToolExecutionError(tool_name, f"Unexpected error: {exc}") from exc


tool_executor = ToolExecutor()
