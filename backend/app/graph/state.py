from typing import TypedDict, List, Dict, Optional


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
    agent_outputs: Dict[str, str]

    # Final answer returned to frontend
    final_response: str