from functools import lru_cache
from config.settings import Settings
from llm.providers.anthropic import AnthropicProvider
from agent.tools.registry import ToolRegistry
from agent.tools.web_search import WebSearchTool
from agent.tools.calculator import CalculatorTool
from agent.tools.file_handler import FileHandlerTool
from agent.core.planner import Planner
from agent.core.executor import Executor
from agent.core.memory import MemoryManager
from agent.core.agent import Agent


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_llm():
    s = get_settings()
    return AnthropicProvider(api_key=s.anthropic_api_key)


def get_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("web_search", WebSearchTool())
    registry.register("calculator", CalculatorTool())
    registry.register("file_handler", FileHandlerTool())
    return registry


def get_agent() -> Agent:
    llm = get_llm()
    registry = get_registry()
    planner = Planner(llm)
    executor = Executor(registry, llm)
    memory = MemoryManager()
    return Agent(planner, executor, memory)
