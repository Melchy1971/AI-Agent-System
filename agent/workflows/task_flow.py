from agent.core.agent import Agent
from agent.core.state import AgentState
from agent.workflows.base_workflow import BaseWorkflow


class TaskFlow(BaseWorkflow):
    """Single-task execution: plan → execute → done."""

    def __init__(self, agent: Agent):
        self._agent = agent

    def run(self, task: str) -> AgentState:
        return self._agent.run(task)
