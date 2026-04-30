from __future__ import annotations
from typing import Any
from agent.tools.base_tool import BaseTool


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def exists(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def schema_summary(self) -> str:
        lines = []
        for tool in self._tools.values():
            schema = tool.schema()
            args = ""
            if "input_schema" in schema:
                props = schema["input_schema"].get("properties", {})
                args = ", ".join(
                    f"{k}: {v.get('type', 'any')}"
                    for k, v in props.items()
                )
            lines.append(f"- {tool.name}({args}): {tool.description}")
        return "\n".join(lines)

    def all_schemas(self) -> list[dict[str, Any]]:
        return [t.schema() for t in self._tools.values()]
