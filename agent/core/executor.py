from __future__ import annotations
import logging
import time
from typing import Any

from agent.core.state import PlanAction, ToolCall, ToolResult
from agent.tools.registry import ToolRegistry

log = logging.getLogger(__name__)


class Executor:
    def __init__(self, registry: ToolRegistry):
        self._registry = registry

    def execute(self, action: PlanAction) -> tuple[ToolCall, ToolResult]:
        call = ToolCall(tool_name=action.tool_name, args=action.args)
        log.debug("→ Tool call [%s] %s args=%s", call.call_id, call.tool_name, call.args)

        tool = self._registry.get(action.tool_name)
        if tool is None:
            result = ToolResult(
                call_id=call.call_id,
                tool_name=action.tool_name,
                success=False,
                error=f"Tool not found in registry: {action.tool_name!r}",
            )
            log.warning("✗ [%s] tool not found", call.call_id)
            return call, result

        t0 = time.perf_counter()
        try:
            output = tool.execute(**action.args)
            duration = (time.perf_counter() - t0) * 1000
            result = ToolResult(
                call_id=call.call_id,
                tool_name=action.tool_name,
                success=True,
                output=output,
                duration_ms=round(duration, 2),
            )
            log.debug("✓ [%s] %.1f ms → %s", call.call_id, duration, str(output)[:120])

        except ValueError as exc:
            duration = (time.perf_counter() - t0) * 1000
            result = ToolResult(
                call_id=call.call_id,
                tool_name=action.tool_name,
                success=False,
                error=f"Invalid input: {exc}",
                duration_ms=round(duration, 2),
            )
            log.warning("✗ [%s] input error: %s", call.call_id, exc)

        except Exception as exc:
            duration = (time.perf_counter() - t0) * 1000
            result = ToolResult(
                call_id=call.call_id,
                tool_name=action.tool_name,
                success=False,
                error=f"Execution error: {type(exc).__name__}: {exc}",
                duration_ms=round(duration, 2),
            )
            log.error("✗ [%s] unexpected error: %s", call.call_id, exc, exc_info=True)

        return call, result
