from abc import ABC, abstractmethod
from agent.core.state import AgentState


class BaseWorkflow(ABC):
    @abstractmethod
    def run(self, task: str) -> AgentState:
        """Execute the workflow and return final state."""
