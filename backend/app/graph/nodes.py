from app.graph.state import AgentState
from app.core.agent_registry import registry
from app.executor.agent_executor import agent_executor


def router_node(state: AgentState):

    result = registry.router.route(
        state["user_input"]
    )

    state["task_type"] = result.task_type

    state["current_agent"] = "Router"

    state["agent_outputs"]["router"] = result.reason

    return state


def planner_node(state: AgentState):

    result = registry.planner.plan(
        user_input=state["user_input"],
        task_type=state["task_type"]
    )

    state["execution_plan"] = result.steps

    state["current_agent"] = "Planner"

    state["agent_outputs"]["planner"] = result.model_dump()

    state["final_response"] = result.model_dump()

    return state

def supervisor_node(state: AgentState):

    planner_data = state["agent_outputs"]["planner"]

    result = registry.supervisor.decide(
        goal=planner_data["goal"],
        steps=planner_data["steps"]
    )

    state["supervisor_tasks"] = [
        task.model_dump()
        for task in result.tasks
    ]

    state["current_agent"] = "Supervisor"

    state["agent_outputs"]["supervisor"] = result.model_dump()

    return state


def execute_agents_node(state):

    tasks = state["supervisor_tasks"]

    outputs = []

    for task in tasks:

        result = agent_executor.execute(task, state)

        outputs.append({
            "task": task,
            "result": result
        })

    state["agent_outputs"]["execution"] = outputs

    state["current_agent"] = "Executor"

    return state