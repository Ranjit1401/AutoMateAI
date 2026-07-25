from app.core.agent_registry import registry


class AgentExecutor:

    def execute(self, task, state):

        agent_name = task["agent"]

        action = task["action"]

        agent = registry.get(agent_name)

        if agent is None:
            raise ValueError(f"Unknown agent: {agent_name}")

        return agent.execute(action, state)


agent_executor = AgentExecutor()