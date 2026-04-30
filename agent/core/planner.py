from __future__ import annotations
import json
import logging
from typing import Any

from pydantic import ValidationError

from agent.core.errors import PlannerError
from agent.core.state import PlanAction
from agent.tools.registry import ToolRegistry

log = logging.getLogger(__name__)


def _build_prompt(tools: str, task: str) -> str:
    return (
        "Return a JSON array of action objects. Each object must have:\n"
        '  {"step": <int>, "description": "<str>", "tool_name": "<str>", "args": {...}}\n\n'
        f"Available tools:\n{tools}\n\n"
        f"Task: {task}\n\n"
        "Constraints:\n"
        "- Use only tools listed above.\n"
        "- args must match the tool input parameters exactly.\n"
        "- Return ONLY the JSON array — no prose, no markdown fences."
    )


class Planner:
    def __init__(self, llm_client, registry: ToolRegistry):
        self._llm = llm_client
        self._registry = registry

    def plan(self, task: str, context: list[dict] | None = None) -> list[PlanAction]:
        prompt = _build_prompt(self._registry.schema_summary(), task)
        raw = self._llm.complete(prompt)
        log.debug("Planner LLM raw: %s", raw[:300])

        actions = self._parse(raw, task)
        validated = self._validate_against_registry(actions)

        if not validated:
            raise PlannerError(f"Planner produced no valid actions for: {task!r}")

        log.debug("Plan: %d steps — %s", len(validated), [a.tool_name for a in validated])
        return validated

    def _parse(self, raw: str, task: str) -> list[PlanAction]:
        text = raw.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(l for l in lines if not l.startswith("```")).strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            log.warning("Planner returned invalid JSON — using fallback")
            return self._fallback(task)

        if not isinstance(data, list):
            log.warning("Planner JSON is not a list — using fallback")
            return self._fallback(task)

        actions: list[PlanAction] = []
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                log.warning("Plan item %d is not a dict, skipping", i)
                continue
            try:
                actions.append(PlanAction(**item))
            except (ValidationError, TypeError) as exc:
                log.warning("Plan item %d invalid: %s — skipping", i, exc)

        return actions

    def _fallback(self, task: str) -> list[PlanAction]:
        return [
            PlanAction(
                step=1,
                description=f"Handle: {task}",
                tool_name="calculator" if any(c.isdigit() for c in task) else "",
                args={},
            )
        ]

    def _validate_against_registry(self, actions: list[PlanAction]) -> list[PlanAction]:
        valid: list[PlanAction] = []
        for action in actions:
            if not action.tool_name:
                log.warning("Plan step %d has no tool_name — skipping", action.step)
                continue
            if not self._registry.exists(action.tool_name):
                log.warning("Plan step %d: unknown tool %r — skipping", action.step, action.tool_name)
                continue
            valid.append(action)
        return valid
