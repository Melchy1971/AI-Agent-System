from typing import Any
from agent.tools.base_tool import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"

    def run(self, input_data) -> list[dict[str, Any]]:
        if isinstance(input_data, dict):
            query = input_data["query"]
            max_results = input_data.get("max_results", 5)
        else:
            query = input_data
            max_results = 5
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))
        except ImportError:
            raise RuntimeError("duckduckgo_search is not installed.")
