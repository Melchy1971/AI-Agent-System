import pytest
from agent.tools.registry import ToolRegistry
from agent.tools.calculator import CalculatorTool
from agent.core.executor import Executor
from agent.core.state import PlanAction


@pytest.fixture
def executor():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    return Executor(registry)


def make_action(tool, args, step=1):
    return PlanAction(step=step, description="test", tool_name=tool, args=args)


def test_successful_execution(executor):
    action = make_action("calculator", {"expression": "6 * 7"})
    call, result = executor.execute(action)
    assert result.success is True
    assert result.output["result"] == 42.0
    assert result.duration_ms >= 0


def test_unknown_tool_returns_failure(executor):
    action = make_action("nonexistent", {})
    call, result = executor.execute(action)
    assert result.success is False
    assert "not found" in result.error


def test_invalid_input_returns_failure(executor):
    action = make_action("calculator", {"expression": "import os"})
    call, result = executor.execute(action)
    assert result.success is False
    assert result.error is not None


def test_division_by_zero_returns_failure(executor):
    action = make_action("calculator", {"expression": "1 / 0"})
    call, result = executor.execute(action)
    assert result.success is False
    assert "zero" in result.error.lower()


def test_call_id_matches(executor):
    action = make_action("calculator", {"expression": "1 + 1"})
    call, result = executor.execute(action)
    assert call.call_id == result.call_id


def test_never_raises(executor):
    """Executor must never propagate exceptions."""
    for expr in ["", "???", "None", "1/0", "x + 1"]:
        action = make_action("calculator", {"expression": expr})
        call, result = executor.execute(action)  # must not raise
        assert isinstance(result.success, bool)
