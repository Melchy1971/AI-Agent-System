from agent.core.memory import MemoryManager


class MemoryController:
    def __init__(self, memory: MemoryManager):
        self._memory = memory

    def recent(self, n: int = 10) -> list[dict]:
        return self._memory.recent(n)
