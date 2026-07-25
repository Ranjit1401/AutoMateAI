from langgraph.graph import StateGraph, END

from app.graph.state import AgentState

from app.graph.nodes import (
    router_node,
    planner_node
)

builder = StateGraph(AgentState)

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "planner",
    planner_node
)

builder.set_entry_point("router")

builder.add_edge(
    "router",
    "planner"
)

builder.add_edge(
    "planner",
    END
)

graph = builder.compile()