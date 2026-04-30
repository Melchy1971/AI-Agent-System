from __future__ import annotations
import hashlib
import json
import logging
from typing import Any

from agent.core.errors import AgentError, PlannerError
from agent.core.executor import Executor
from agent.core.memory import MemoryManager
from agent.core.planner import Planner
from agent.core.state import AgentState, AgentStep, Status

log = logging.getLogger(__name__)

_LOOP_WINDOW = 3      # check last N steps for repetition
_DEFAULT_MAX = 20


class Agent:
    """
    Execution loop: plan → [execute → record] × N → respond.

    Guarantees:
    - Never crashes on tool errors (Executor absorbs them as ToolResult).
    - Stops on loop detection (same tool+args repeated _LOOP_WINDOW times).
    - Respects max_steps from config or default.
    - Returns AgentState in every code path.
    """

    def __init__(
        self,
        planner: Planner,
        executor: Executor,
        memory: MemoryManager,
        max_steps: int = _DEFAULT_MAX,
        llm_client=None,
    ):
        self.planner = planner
        self.executor = executor
        self.memory = memory
        self.max_steps = max_steps
        self._llm = llm_client

    # ── Public ─────────────────────────────────────────────────────────────────

    def run(self, task: str) -> AgentState:
        state = AgentState(task=task, status=Status.PLANNING)
        log.debug("Agent run [%s] task=%r", state.run_id, task[:80])

        try:
            context = self.memory.recent()
            state.plan = self.planner.plan(task, context)
        except PlannerError as exc:
            return self._fail(state, str(exc))
        except Exception as exc:
            return self._fail(state, f"Planning failed unexpectedly: {exc}")

        state.status = Status.EXECUTING
        seen: list[str] = []

        while not state.is_complete and state.current_step < self.max_steps:
            action = state.plan[state.current_step]

            # Loop detection
            fingerprint = self._fingerprint(action.tool_name, action.args)
            seen.append(fingerprint)
            if len(seen) >= _LOOP_WINDOW and len(set(seen[-_LOOP_WINDOW:])) == 1:
                state.loop_detected = True
                log.warning("Loop detected at step %d — same call repeated %d times",
                            state.current_step, _LOOP_WINDOW)
                break

            call, result = self.executor.execute(action)
            step = AgentStep(
                step_number=state.current_step + 1,
                action=action,
                tool_call=call,
                result=result,
            )
            state.record_step(step)
            self.memory.add({
                "step": action.description,
                "tool": action.tool_name,
                "output": result.output,
                "success": result.success,
            })

        state.status = Status.DONE
        state.final_response = self._generate_response(state)
        log.debug("Run [%s] done — %d steps, %d failed",
                  state.run_id, len(state.steps), len(state.failed_steps))
        return state

    # ── Internals ───────────────────────────────────────────────────────────────

    @staticmethod
    def _fingerprint(tool_name: str, args: dict) -> str:
        key = json.dumps({"t": tool_name, "a": args}, sort_keys=True)
        return hashlib.md5(key.encode()).hexdigest()[:8]

    @staticmethod
    def _fail(state: AgentState, message: str) -> AgentState:
        state.status = Status.ERROR
        state.error = message
        log.error("Agent failed: %s", message)
        return state

    def _generate_response(self, state: AgentState) -> str:
        successful = [s for s in state.steps if s.result and s.result.success]
        if not successful:
            errors = [s.result.error for s in state.steps if s.result and s.result.error]
            return f"No steps succeeded. Errors: {'; '.join(errors)}" if errors else "No output."

        outputs = []
        for s in successful:
            out = s.result.output
            if isinstance(out, dict) and "result" in out:
                outputs.append(f"{s.action.description}: {out['result']}")
            else:
                outputs.append(f"{s.action.description}: {out}")

        if state.loop_detected:
            outputs.append("[Warning: execution stopped — loop detected]")

        # Use LLM to synthesize if available, else join outputs
        if self._llm and len(successful) > 1:
            summary_prompt = (
                f"Task: {state.task}\n\n"
                f"Results:\n" + "\n".join(outputs) +
                "\n\nWrite a concise final answer in one sentence."
            )
            try:
                return self._llm.complete(summary_prompt)
            except Exception:
                pass

        return " | ".join(outputs)
