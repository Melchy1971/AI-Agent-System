import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.server import create_app
from agent.core.state import AgentState, Status


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_tool_list(client):
    with patch("api.routes.tool_routes.get_registry") as mock_reg:
        mock_reg.return_value.list_names.return_value = ["calculator", "web_search"]
        r = client.get("/tools/")
        assert r.status_code == 200


def test_agent_run(client):
    mock_state = AgentState(status=Status.DONE, results=[])
    with patch("api.routes.agent_routes.get_agent") as mock_agent_dep:
        mock_agent_dep.return_value.run.return_value = mock_state
        r = client.post("/agent/run", json={"task": "test"})
        assert r.status_code == 200
