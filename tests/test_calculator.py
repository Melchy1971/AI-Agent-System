import pytest
from agent.tools.calculator import CalculatorTool


@pytest.fixture
def calc():
    return CalculatorTool()


def test_basic_arithmetic(calc):
    assert calc.run(expression="2 + 2")["result"] == 4.0
    assert calc.run(expression="10 - 3")["result"] == 7.0
    assert calc.run(expression="6 * 7")["result"] == 42.0
    assert calc.run(expression="10 / 4")["result"] == 2.5


def test_compound(calc):
    assert calc.run(expression="25 * 12 + 5")["result"] == 305.0


def test_power(calc):
    assert calc.run(expression="2 ** 10")["result"] == 1024.0


def test_mod(calc):
    assert calc.run(expression="17 % 5")["result"] == 2.0


def test_unary(calc):
    assert calc.run(expression="-5 + 10")["result"] == 5.0


def test_floordiv(calc):
    assert calc.run(expression="7 // 2")["result"] == 3.0


def test_allowed_functions(calc):
    assert calc.run(expression="abs(-9)")["result"] == 9.0
    assert calc.run(expression="round(3.7)")["result"] == 4.0
    assert calc.run(expression="min(3, 1, 2)")["result"] == 1.0
    assert calc.run(expression="max(3, 1, 2)")["result"] == 3.0


def test_division_by_zero(calc):
    with pytest.raises(ValueError, match="zero"):
        calc.run(expression="1 / 0")


def test_invalid_syntax(calc):
    with pytest.raises(ValueError, match="Syntax"):
        calc.run(expression="2 +* 3")


def test_no_eval_import(calc):
    with pytest.raises(ValueError):
        calc.run(expression="__import__('os').system('ls')")


def test_no_string_constant(calc):
    with pytest.raises(ValueError):
        calc.run(expression="'hello'")


def test_no_arbitrary_function(calc):
    with pytest.raises(ValueError, match="not allowed"):
        calc.run(expression="print(1)")


def test_schema_present():
    t = CalculatorTool()
    schema = t.schema()
    assert schema["name"] == "calculator"
    assert "input_schema" in schema
    assert "output_schema" in schema


def test_validate_input_rejects_missing(calc):
    with pytest.raises(ValueError):
        calc.validate_input()  # expression is required


def test_execute_validates_then_runs(calc):
    result = calc.execute(expression="3 * 3")
    assert result["result"] == 9.0
