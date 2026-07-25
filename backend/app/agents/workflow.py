from langgraph.graph import StateGraph
from app.graph.state import AgentState
from app.graph.nodes import (
    classify_node,
    planner_node,
    finish_node,
)

builder = StateGraph(AgentState)

builder.add_node("classify", classify_node)

builder.add_node("planner", planner_node)

builder.add_node("finish", finish_node)

builder.set_entry_point("classify")

builder.add_edge("classify", "planner")

builder.add_edge("planner", "finish")

builder.set_finish_point("finish")

graph = builder.compile()