from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    session_id: str

    user_input: str

    conversation_history: List[Dict[str, str]]

    user_id: Optional[str]

    task_type: str

    execution_plan: List[str]

    current_agent: str

    supervisor_tasks: List[Dict[str, str]]

    agent_outputs: Dict[str, Any]

    final_response: Any