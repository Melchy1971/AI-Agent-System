import pytest
from memory.short_term.buffer import ShortTermMemory


def test_short_term_memory_adds_items():
    buf = ShortTermMemory()
    for i in range(5):
        buf.add({"n": i})
    data = buf.get()
    assert len(data) == 5
    assert data[-1]["n"] == 4


def test_short_term_memory_returns_underlying_data():
    buf = ShortTermMemory()
    buf.add({"x": 1})
    assert buf.get() == [{"x": 1}]
