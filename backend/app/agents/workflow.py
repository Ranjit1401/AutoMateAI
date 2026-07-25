from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.graph.nodes import (
    router_node,
    planner_node,
    supervisor_node,
    execute_agents_node,
    response_node,
)

builder = StateGraph(AgentState)

# Nodes
builder.add_node("router", router_node)
builder.add_node("planner", planner_node)
builder.add_node("supervisor", supervisor_node)
builder.add_node("execute_agents", execute_agents_node)
builder.add_node("response", response_node)

# Flow
builder.add_edge(START, "router")
builder.add_edge("router", "planner")
builder.add_edge("planner", "supervisor")
builder.add_edge("supervisor", "execute_agents")
builder.add_edge("execute_agents", "response")
builder.add_edge("response", END)

graph = builder.compile()