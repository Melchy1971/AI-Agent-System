from agent.core.agent import Agent
from agent.core.state import AgentState
from agent.workflows.base_workflow import BaseWorkflow


class ResearchFlow(BaseWorkflow):
    """
    Research workflow: search → collect → synthesize.
    Runs multiple search subtasks and aggregates results.
    """

    def __init__(self, agent: Agent, search_rounds: int = 3):
        self._agent = agent
        self._rounds = search_rounds

    def run(self, task: str) -> AgentState:
        results = []
        for i in range(self._rounds):
            state = self._agent.run(f"Search round {i + 1}: {task}")
            results.extend(state.results)

        synthesis_state = self._agent.run(
            f"Synthesize the following research results into a final answer: {results}"
        )
        return synthesis_state
