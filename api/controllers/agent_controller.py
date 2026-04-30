from agent.core.agent import Agent
from agent.core.state import AgentState


class AgentController:
    def __init__(self, agent: Agent):
        self._agent = agent

    def execute(self, task: str) -> AgentState:
        return self._agent.run(task)
