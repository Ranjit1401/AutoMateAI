from typing import TypedDict, List, Dict, Optional , Any


class AgentState(TypedDict):
    # Original user message
    user_input: str

    # User ID (for memory later)
    user_id: Optional[str]

    # Task detected by Router Agent
    task_type: str

    # Planner output
    execution_plan: List[str]

    # Which agent is currently running
    current_agent: str

    # Outputs from every agent
    agent_outputs: Dict[str, Any]
    supervisor_tasks: List[Dict[str, str]]


    # Final answer returned to frontend
    final_response: Any