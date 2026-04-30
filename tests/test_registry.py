import pytest
from agent.tools.registry import ToolRegistry
from agent.tools.calculator import CalculatorTool
from agent.tools.file_handler import FileHandlerTool


@pytest.fixture
def registry():
    r = ToolRegistry()
    r.register(CalculatorTool())
    r.register(FileHandlerTool())
    return r


def test_exists(registry):
    assert registry.exists("calculator")
    assert registry.exists("file_handler")
    assert not registry.exists("nonexistent")


def test_get_returns_tool(registry):
    tool = registry.get("calculator")
    assert tool is not None
    assert tool.name == "calculator"


def test_get_returns_none_for_unknown(registry):
    assert registry.get("unknown_tool") is None


def test_list_tools(registry):
    tools = registry.list_tools()
    assert "calculator" in tools
    assert "file_handler" in tools


def test_schema_summary_contains_names(registry):
    summary = registry.schema_summary()
    assert "calculator" in summary
    assert "file_handler" in summary


def test_all_schemas(registry):
    schemas = registry.all_schemas()
    names = [s["name"] for s in schemas]
    assert "calculator" in names


def test_register_overwrites(registry):
    class MyCalc(CalculatorTool):
        description = "overwritten"
    registry.register(MyCalc())
    assert registry.get("calculator").description == "overwritten"
