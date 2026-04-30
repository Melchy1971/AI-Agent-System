from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Type
from pydantic import BaseModel, ValidationError


class BaseTool(ABC):
    name: str
    description: str
    input_schema: Type[BaseModel] | None = None
    output_schema: Type[BaseModel] | None = None

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """Core tool logic. Raise ValueError on bad input, RuntimeError on execution failure."""

    def validate_input(self, **kwargs) -> dict[str, Any]:
        """Validate kwargs against input_schema. Returns validated dict."""
        if self.input_schema is None:
            return kwargs
        try:
            model = self.input_schema(**kwargs)
            return model.model_dump()
        except ValidationError as exc:
            raise ValueError(f"[{self.name}] invalid input: {exc}") from exc

    def execute(self, **kwargs) -> Any:
        """Validate input then run. Called by Executor — never call run() directly."""
        validated = self.validate_input(**kwargs)
        return self.run(**validated)

    def schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {"name": self.name, "description": self.description}
        if self.input_schema is not None:
            schema["input_schema"] = self.input_schema.model_json_schema()
        if self.output_schema is not None:
            schema["output_schema"] = self.output_schema.model_json_schema()
        return schema
