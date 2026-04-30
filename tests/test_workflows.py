from unittest.mock import MagicMock
from agent.workflows.task_flow import TaskFlow
from agent.core.state import AgentState, Status


def test_task_flow_delegates():
    agent = MagicMock()
    state = AgentState(status=Status.DONE)
    agent.run.return_value = state
    flow = TaskFlow(agent)
    result = flow.run("do something")
    assert result.status == Status.DONE
    agent.run.assert_called_once_with("do something")
