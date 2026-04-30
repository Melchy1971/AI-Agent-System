import json
import pytest
from unittest.mock import MagicMock
from agent.core.agent import Agent
from agent.core.executor import Executor
from agent.core.memory import MemoryManager
from agent.core.planner import Planner
from agent.core.state import AgentState, Status
from agent.tools.calculator import CalculatorTool
from agent.tools.registry import ToolRegistry


def make_registry():
    r = ToolRegistry()
    r.register(CalculatorTool())
    return r


def make_agent(plan_response: str = None, max_steps: int = 10):
    registry = make_registry()
    if plan_response is None:
        plan_response = json.dumps([{
            "step": 1,
            "description": "Calculate 6*7",
            "tool_name": "calculator",
            "args": {"expression": "6 * 7"},
        }])
    llm = MagicMock()
    llm.complete.return_value = plan_response
    planner = Planner(llm, registry)
    executor = Executor(registry)
    memory = MemoryManager()
    return Agent(planner, executor, memory, max_steps=max_steps)


def test_successful_run():
    agent = make_agent()
    state = agent.run("What is 6 * 7?")
    assert state.status == Status.DONE
    assert len(state.steps) == 1
    assert state.steps[0].result.success is True
    assert state.steps[0].result.output["result"] == 42.0


def test_final_response_contains_result():
    agent = make_agent()
    state = agent.run("What is 6 * 7?")
    assert "42" in str(state.final_response)


def test_planner_error_returns_error_state():
    from agent.core.errors import PlannerError
    registry = make_registry()
    planner = MagicMock()
    planner.plan.side_effect = PlannerError("no plan")
    executor = Executor(registry)
    memory = MemoryManager()
    agent = Agent(planner, executor, memory)
    state = agent.run("impossible")
    assert state.status == Status.ERROR
    assert "no plan" in state.error


def test_max_steps_respected():
    plan = json.dumps([
        {"step": i+1, "description": f"step {i+1}", "tool_name": "calculator",
         "args": {"expression": str(i+1)}}
        for i in range(15)
    ])
    agent = make_agent(plan_response=plan, max_steps=5)
    state = agent.run("run many steps")
    assert len(state.steps) <= 5


def test_loop_detection():
    plan = json.dumps([
        {"step": i+1, "description": "same", "tool_name": "calculator",
         "args": {"expression": "1+1"}}
        for i in range(10)
    ])
    agent = make_agent(plan_response=plan, max_steps=20)
    state = agent.run("loop test")
    assert state.loop_detected is True


def test_unknown_tool_does_not_crash():
    plan = json.dumps([{
        "step": 1, "description": "bad", "tool_name": "nonexistent", "args": {}
    }])
    # planner will filter it out → PlannerError
    agent = make_agent(plan_response=plan)
    state = agent.run("test")
    # either ERROR (planner filtered) or DONE with failed step
    assert state.status in (Status.ERROR, Status.DONE)


def test_state_tracks_failed_steps():
    plan = json.dumps([
        {"step": 1, "description": "divide", "tool_name": "calculator",
         "args": {"expression": "1 / 0"}},
    ])
    agent = make_agent(plan_response=plan)
    state = agent.run("divide by zero")
    assert len(state.failed_steps) == 1
