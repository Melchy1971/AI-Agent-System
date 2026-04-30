from typing import Any
from agent.tools.base_tool import BaseTool


class DatabaseTool(BaseTool):
    name = "database"
    description = "Execute a SQL query. Args: query (str). Returns list of row dicts."

    def __init__(self, connection_string: str):
        self._conn_str = connection_string
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from sqlalchemy import create_engine
            self._engine = create_engine(self._conn_str)
        return self._engine

    def run(self, query: str) -> list[dict[str, Any]]:
        from sqlalchemy import text
        with self._get_engine().connect() as conn:
            result = conn.execute(text(query))
            return [dict(row._mapping) for row in result]
