# tests/test_core.py

import pytest
from box_manager import BoxManager


def test_decorator_runs_function(monkeypatch):
    manager = BoxManager()
    executed = {}

    @manager.with_orchestration()
    def dummy_task():
        executed["done"] = True

    dummy_task()
    assert executed.get("done") is True
