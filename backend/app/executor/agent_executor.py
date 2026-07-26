from app.core.agent_registry import registry


class AgentExecutionError(Exception):
    pass


class AgentExecutor:
    def execute(self, task: dict, state: dict):
        agent_name = task["agent"]
        action = task["action"]

        agent = registry.get(agent_name)
        if agent is None:
            raise AgentExecutionError(f"Unknown agent: {agent_name}")

        return agent.execute(action, state)


agent_executor = AgentExecutor()
