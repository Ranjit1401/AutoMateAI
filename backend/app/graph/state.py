from typing import Any, TypedDict


class AgentState(TypedDict):
    session_id: str
    user_input: str
    conversation_history: list[dict[str, str]]
    long_term_memory: list[str]
    user_id: str | None
    task_type: str
    execution_plan: list[str]
    current_agent: str
    supervisor_tasks: list[dict[str, str]]
    agent_outputs: dict[str, Any]
    final_response: Any
