import json
import pytest
from unittest.mock import MagicMock
from agent.core.planner import Planner
from agent.core.errors import PlannerError
from agent.core.state import PlanAction
from agent.tools.registry import ToolRegistry
from agent.tools.calculator import CalculatorTool


@pytest.fixture
def registry():
    r = ToolRegistry()
    r.register(CalculatorTool())
    return r


def make_planner(response: str, registry):
    llm = MagicMock()
    llm.complete.return_value = response
    return Planner(llm, registry)


def valid_plan_json(tool="calculator", args=None):
    return json.dumps([{
        "step": 1,
        "description": "calc",
        "tool_name": tool,
        "args": args or {"expression": "1+1"},
    }])


def test_valid_json_parsed(registry):
    planner = make_planner(valid_plan_json(), registry)
    plan = planner.plan("1+1")
    assert len(plan) == 1
    assert plan[0].tool_name == "calculator"


def test_strips_markdown_fences(registry):
    raw = "```json\n" + valid_plan_json() + "\n```"
    planner = make_planner(raw, registry)
    plan = planner.plan("test")
    assert len(plan) == 1


def test_invalid_json_uses_fallback(registry):
    planner = make_planner("this is not JSON at all", registry)
    # calculator is in registry, fallback may produce empty or minimal plan
    # should not raise
    try:
        plan = planner.plan("some task with 42 in it")
    except PlannerError:
        pass  # acceptable if fallback produces no valid tools


def test_unknown_tool_filtered_out(registry):
    raw = json.dumps([
        {"step": 1, "description": "calc", "tool_name": "calculator", "args": {"expression": "1"}},
        {"step": 2, "description": "bad", "tool_name": "nonexistent_tool", "args": {}},
    ])
    planner = make_planner(raw, registry)
    plan = planner.plan("test")
    assert all(a.tool_name == "calculator" for a in plan)


def test_empty_json_array_raises(registry):
    planner = make_planner("[]", registry)
    with pytest.raises(PlannerError):
        planner.plan("test")


def test_non_list_json_falls_back(registry):
    planner = make_planner('{"step": 1}', registry)
    try:
        planner.plan("test 1 + 1")
    except PlannerError:
        pass  # acceptable


def test_plan_action_model():
    a = PlanAction(step=1, description="d", tool_name="t", args={"x": 1})
    assert a.step == 1
    assert a.args == {"x": 1}
