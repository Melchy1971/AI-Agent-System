from __future__ import annotations
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Status(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    DONE = "done"
    ERROR = "error"


class PlanAction(BaseModel):
    step: int
    description: str
    tool_name: str
    args: dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    call_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    tool_name: str
    args: dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ToolResult(BaseModel):
    call_id: str
    tool_name: str
    success: bool
    output: Any = None
    error: str | None = None
    duration_ms: float = 0.0


class AgentStep(BaseModel):
    step_number: int
    action: PlanAction
    tool_call: ToolCall | None = None
    result: ToolResult | None = None


class AgentState(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    task: str
    status: Status = Status.IDLE
    plan: list[PlanAction] = Field(default_factory=list)
    steps: list[AgentStep] = Field(default_factory=list)
    current_step: int = 0
    final_response: str | None = None
    error: str | None = None
    loop_detected: bool = False

    @property
    def is_complete(self) -> bool:
        return self.current_step >= len(self.plan)

    @property
    def failed_steps(self) -> list[AgentStep]:
        return [s for s in self.steps if s.result and not s.result.success]

    def record_step(self, step: AgentStep) -> None:
        self.steps.append(step)
        self.current_step += 1

    def last_results(self, n: int = 5) -> list[dict[str, Any]]:
        return [
            {"tool": s.action.tool_name, "output": s.result.output if s.result else None}
            for s in self.steps[-n:]
        ]
