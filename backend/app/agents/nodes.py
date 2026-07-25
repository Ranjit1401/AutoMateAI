from app.graph.state import AgentState
from app.agents.master_agent import MasterAgent
from app.agents.planner_agent import PlannerAgent


master = MasterAgent()

planner = PlannerAgent()


def classify_node(state: AgentState):

    task = master.detect_task(state["user_input"])

    state["task_type"] = task

    state["current_agent"] = "Planner"

    return state


def planner_node(state: AgentState):

    plan = planner.execute(state["user_input"])

    state["execution_plan"] = plan

    return state


def finish_node(state: AgentState):

    result = "\n".join(state["execution_plan"])

    state["final_response"] = result

    return state