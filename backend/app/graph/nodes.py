from app.core.agent_registry import registry
from app.executor.agent_executor import agent_executor
from app.graph.state import AgentState


def _context_enriched_input(state: AgentState) -> str:
    """Folds long-term memory and recent conversation history into the text
    handed to the router/planner, so both actually influence behavior
    instead of being stored and ignored (the previous version fetched
    conversation_history into state but no agent ever read it)."""
    parts = []

    if state.get("long_term_memory"):
        parts.append("Known facts about this user:\n" + "\n".join(f"- {m}" for m in state["long_term_memory"]))

    history = state.get("conversation_history") or []
    if len(history) > 1:
        recent = history[-6:-1]  # exclude the just-added current message
        if recent:
            formatted = "\n".join(f"{m['role']}: {m['content']}" for m in recent)
            parts.append(f"Recent conversation:\n{formatted}")

    parts.append(f"Current message:\n{state['user_input']}")
    return "\n\n".join(parts)


def router_node(state: AgentState) -> AgentState:
    router = registry.get("router")
    result = router.route(_context_enriched_input(state))

    state["task_type"] = result.task_type
    state["current_agent"] = "Router"
    state["agent_outputs"]["router"] = result.model_dump()
    return state


def planner_node(state: AgentState) -> AgentState:
    planner = registry.get("planner")
    result = planner.plan(user_input=_context_enriched_input(state), task_type=state["task_type"])

    state["execution_plan"] = result.steps
    state["current_agent"] = "Planner"
    state["agent_outputs"]["planner"] = result.model_dump()
    return state


def supervisor_node(state: AgentState) -> AgentState:
    supervisor = registry.get("supervisor")
    planner_data = state["agent_outputs"]["planner"]

    result = supervisor.decide(goal=planner_data["goal"], steps=planner_data["steps"])

    state["supervisor_tasks"] = [task.model_dump() for task in result.tasks]
    state["current_agent"] = "Supervisor"
    state["agent_outputs"]["supervisor"] = result.model_dump()
    return state


def execute_agents_node(state: AgentState) -> AgentState:
    tasks = state["supervisor_tasks"]
    outputs = []

    for task in tasks:
        try:
            result = agent_executor.execute(task, state)
        except Exception as exc:  # noqa: BLE001 — one failing agent must not
            # abort the whole run; capture it and let the response agent
            # report partial results instead.
            result = {"error": str(exc)}
        outputs.append({"task": task, "result": result})

    state["agent_outputs"]["execution"] = outputs
    state["current_agent"] = "Executor"
    return state


def response_node(state: AgentState) -> AgentState:
    response_agent = registry.get("response")
    state["final_response"] = response_agent.generate(state)
    return state
