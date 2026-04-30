#!/usr/bin/env python3
"""
End-to-end CLI runner — uses a mock LLM so no API key is needed.

Usage:
    python scripts/run_agent.py "What is 25 * 12 + 5?"
    python scripts/run_agent.py "Calculate 100 / 4"
    python scripts/run_agent.py "abs(-42) + round(3.7)"
"""
import sys
import json
import re
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.core.logger import setup_logging
from agent.core.planner import Planner
from agent.core.executor import Executor
from agent.core.memory import MemoryManager
from agent.core.agent import Agent
from agent.tools.registry import ToolRegistry
from agent.tools.calculator import CalculatorTool
from agent.tools.file_handler import FileHandlerTool


# ── Mock LLM ──────────────────────────────────────────────────────────────────

# Match expressions like "25 * 12 + 5", "100/4", "abs(-42)" — requires an operator or function
_EXPR_RE = re.compile(
    r"""
    (?:abs|round|min|max|int|float)\s*\([^)]+\)   # function call
    |
    -?\d+(?:\.\d+)?                                 # leading number
    (?:\s*[\+\-\*\/\%\*\*\/\/]+\s*-?\d+(?:\.\d+)?)+ # followed by op+number pairs
    """,
    re.VERBOSE,
)


class MockLLM:
    """Deterministic LLM for local testing — no API key required."""

    def complete(self, prompt: str) -> str:
        # Extract task line from planner prompt
        task = prompt
        for line in prompt.splitlines():
            if line.startswith("Task:"):
                task = line.replace("Task:", "").strip()
                break

        match = _EXPR_RE.search(task)
        expression = match.group(0).strip() if match else "0"
        expression = expression.replace("^", "**")

        plan = [{"step": 1, "description": f"Calculate: {expression}",
                  "tool_name": "calculator", "args": {"expression": expression}}]
        return json.dumps(plan)


# ── Wiring ─────────────────────────────────────────────────────────────────────

def build_agent(max_steps: int = 10) -> Agent:
    setup_logging()
    logging.getLogger("agent.core.agent").setLevel(logging.DEBUG)
    logging.getLogger("agent.core.executor").setLevel(logging.DEBUG)
    logging.getLogger("agent.core.planner").setLevel(logging.DEBUG)

    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(FileHandlerTool())

    llm = MockLLM()
    planner = Planner(llm, registry)
    executor = Executor(registry)
    memory = MemoryManager()
    return Agent(planner, executor, memory, max_steps=max_steps, llm_client=llm)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    task = " ".join(sys.argv[1:]) or "What is 25 * 12 + 5?"
    print(f"\nTask: {task}")
    print("─" * 50)

    agent = build_agent()
    state = agent.run(task)

    print(f"\nStatus : {state.status}")
    print(f"Steps  : {len(state.steps)}")
    for step in state.steps:
        r = step.result
        if r and r.success:
            print(f"  ✓ [{r.tool_name}] {r.output}  ({r.duration_ms:.1f}ms)")
        elif r:
            print(f"  ✗ [{r.tool_name}] {r.error}")

    print(f"\nAnswer : {state.final_response}")
    if state.error:
        print(f"Error  : {state.error}", file=sys.stderr)


if __name__ == "__main__":
    main()
