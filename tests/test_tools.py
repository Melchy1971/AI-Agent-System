import pytest
from agent.tools.calculator import CalculatorTool
from agent.tools.file_handler import FileHandlerTool
import tempfile, os


def test_calculator_basic():
    tool = CalculatorTool()
    assert tool.run("2 + 2") == "4"
    assert tool.run("10 * 3") == "30"


def test_calculator_invalid():
    tool = CalculatorTool()
    assert tool.run("import os") != ""


def test_file_handler_write_read():
    tool = FileHandlerTool()
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.txt")
        tool.run({"action": "write", "path": path, "content": "hello"})
        result = tool.run({"action": "read", "path": path})
        assert result == "hello"
