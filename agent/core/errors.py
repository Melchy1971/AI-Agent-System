class AgentError(Exception):
    """Base exception for all agent errors."""

class PlannerError(AgentError):
    """Raised when planning fails."""

class ExecutionError(AgentError):
    """Raised when a tool execution fails."""
    def __init__(self, message: str, tool_name: str | None = None):
        super().__init__(message)
        self.tool_name = tool_name

class MemoryError(AgentError):
    """Raised on memory read/write failures."""

class WorkflowError(AgentError):
    """Raised when a workflow cannot proceed."""
