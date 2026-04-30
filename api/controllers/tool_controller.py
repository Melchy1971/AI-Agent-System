from agent.tools.registry import ToolRegistry


class ToolController:
    def __init__(self, registry: ToolRegistry):
        self._registry = registry

    def list(self) -> list[str]:
        return self._registry.list_names()
