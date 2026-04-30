from pathlib import Path
from pydantic import BaseModel
from agent.tools.base_tool import BaseTool


class FileInput(BaseModel):
    action: str
    path: str
    content: str = ""


class FileHandlerTool(BaseTool):
    name = "file_handler"
    description = "Read or write files. Args: action ('read'|'write'), path (str), content (str, write only)."
    input_schema = FileInput

    def run(self, action: str, path: str, content: str = "", **_) -> str:
        p = Path(path)
        if action == "read":
            if not p.exists():
                raise ValueError(f"File not found: {path}")
            return p.read_text(encoding="utf-8")
        elif action == "write":
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return f"Written: {p}"
        raise ValueError(f"Unknown action: {action!r}. Use 'read' or 'write'.")
