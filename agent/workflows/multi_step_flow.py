from agent.core.agent import Agent
from agent.core.state import AgentState
from agent.workflows.base_workflow import BaseWorkflow


class MultiStepFlow(BaseWorkflow):
    """
    Executes a sequence of dependent tasks in order.
    Output of step N is injected into the context of step N+1.
    """

    def __init__(self, agent: Agent):
        self._agent = agent

    def run(self, task: str) -> AgentState:
        subtasks = [t.strip() for t in task.split("->") if t.strip()]
        last_state: AgentState | None = None
        for subtask in subtasks:
            if last_state:
                subtask = f"{subtask} [prior result: {last_state.results[-1] if last_state.results else 'none'}]"
            last_state = self._agent.run(subtask)
        return last_state
