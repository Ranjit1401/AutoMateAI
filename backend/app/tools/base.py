"""
Base contract every tool implements. Consolidated from the two near-duplicate
base classes (tools/base.py + tools/base_tool.py) that existed previously.
"""
from abc import ABC, abstractmethod
from typing import Any


class ToolError(Exception):
    """Raised by a tool when it cannot complete its request (bad input,
    upstream API failure, missing credentials, etc). The tool executor
    catches this and turns it into a structured error the agent can react
    to, instead of letting exceptions crash the whole graph run."""


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Run the tool. Raise ToolError on any recoverable failure."""
        raise NotImplementedError
