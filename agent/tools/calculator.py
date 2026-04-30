from __future__ import annotations
import ast
import operator
from typing import Any
from pydantic import BaseModel
from agent.tools.base_tool import BaseTool


class CalcInput(BaseModel):
    expression: str


class CalcOutput(BaseModel):
    result: float
    expression: str


class CalculatorTool(BaseTool):
    name = "calculator"
    description = (
        "Safely evaluate a mathematical expression. "
        "Supports: +, -, *, /, **, %, unary minus, abs(), round(), min(), max(). "
        "No arbitrary code execution."
    )
    input_schema = CalcInput
    output_schema = CalcOutput

    _OPS: dict = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    _FUNCS: dict = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "int": int,
        "float": float,
    }

    def _eval(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError(f"Constant type not allowed: {type(node.value).__name__}")
            return float(node.value)

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._OPS:
                raise ValueError(f"Operator not allowed: {op_type.__name__}")
            left = self._eval(node.left)
            right = self._eval(node.right)
            if op_type is ast.Div and right == 0:
                raise ValueError("Division by zero")
            if op_type is ast.FloorDiv and right == 0:
                raise ValueError("Division by zero")
            return float(self._OPS[op_type](left, right))

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._OPS:
                raise ValueError(f"Unary operator not allowed: {op_type.__name__}")
            return float(self._OPS[op_type](self._eval(node.operand)))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function calls are allowed")
            name = node.func.id
            if name not in self._FUNCS:
                raise ValueError(f"Function not allowed: {name!r}")
            if node.keywords:
                raise ValueError("Keyword arguments not allowed in function calls")
            args = [self._eval(a) for a in node.args]
            return float(self._FUNCS[name](*args))

        raise ValueError(f"Expression node not allowed: {type(node).__name__}")

    def run(self, expression: str, **_) -> dict[str, Any]:
        expr = expression.strip()
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"Syntax error: {exc}") from exc
        result = self._eval(tree.body)
        return {"result": result, "expression": expr}
