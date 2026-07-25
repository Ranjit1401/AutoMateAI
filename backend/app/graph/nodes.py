from app.graph.state import AgentState
from app.core.agent_registry import registry
from app.executor.agent_executor import agent_executor
from app.agents.budget_agent import BudgetAgent

budget_agent = BudgetAgent()
def budget_node(state):

    result = budget_agent.execute(None, state)

    state["agent_outputs"]["budget"] = result

    return state


def router_node(state: AgentState):

    router = registry.get("router")

    result = router.route(
        state["user_input"]
    )

    state["task_type"] = result.task_type
    state["current_agent"] = "Router"
    state["agent_outputs"]["router"] = result.model_dump()

    return state


def planner_node(state: AgentState):

    planner = registry.get("planner")

    result = planner.plan(
        user_input=state["user_input"],
        task_type=state["task_type"]
    )

    print("========== PLANNER RESULT ==========")
    print(result)


    state["execution_plan"] = result.steps
    state["current_agent"] = "Planner"
    state["agent_outputs"]["planner"] = result.model_dump()

    return state


def supervisor_node(state: AgentState):

    supervisor = registry.get("supervisor")

    planner_data = state["agent_outputs"]["planner"]

    result = supervisor.decide(
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


def execute_agents_node(state: AgentState):

    tasks = state["supervisor_tasks"]

    outputs = []

    for task in tasks:

        result = agent_executor.execute(
            task,
            state
        )

        outputs.append({
            "task": task,
            "result": result
        })

    state["agent_outputs"]["execution"] = outputs

    state["current_agent"] = "Executor"

    return state


def response_node(state):

    response_agent = registry.get("response")

    final_response = response_agent.generate(state)

    state["final_response"] = final_response

    return state