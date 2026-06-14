import json
import pytest
from pathlib import Path
from todo.store import add_todo, load_todos, complete_todo, delete_todo, parse_due_date


@pytest.fixture
def tmp_store(tmp_path):
    return tmp_path / "todos.json"


def test_add_and_load(tmp_store):
    add_todo("Buy milk", path=tmp_store)
    add_todo("Walk dog", path=tmp_store)
    todos = load_todos(tmp_store)
    assert len(todos) == 2
    assert todos[0]["title"] == "Buy milk"
    assert todos[1]["title"] == "Walk dog"


def test_complete(tmp_store):
    add_todo("Read book", path=tmp_store)
    result = complete_todo(1, tmp_store)
    assert result is not None
    assert result["done"] is True


def test_complete_missing(tmp_store):
    result = complete_todo(99, tmp_store)
    assert result is None


def test_delete(tmp_store):
    add_todo("Trash", path=tmp_store)
    assert delete_todo(1, tmp_store) is True
    assert load_todos(tmp_store) == []


def test_delete_missing(tmp_store):
    assert delete_todo(99, tmp_store) is False


def test_add_with_due_date(tmp_store):
    add_todo("Buy milk", due="2026-06-20", path=tmp_store)
    todos = load_todos(tmp_store)
    assert todos[0]["due"] == "2026-06-20"


def test_add_without_due_date(tmp_store):
    add_todo("Walk dog", path=tmp_store)
    todos = load_todos(tmp_store)
    assert todos[0]["due"] is None


def test_due_date_validation(tmp_store):
    with pytest.raises(ValueError):
        add_todo("Test", due="not-a-date", path=tmp_store)


def test_backward_compat(tmp_store):
    tmp_store.write_text(json.dumps([{"id": 1, "title": "Old", "done": False}]))
    todos = load_todos(tmp_store)
    assert todos[0].get("due") is None


def test_sort_with_mixed_due_dates():
    todos = [
        {"id": 1, "title": "Tomorrow", "done": False, "due": "2026-06-21"},
        {"id": 2, "title": "No date", "done": False, "due": None},
        {"id": 3, "title": "Today", "done": False, "due": "2026-06-20"},
    ]
    result = sorted(todos, key=lambda t: (t.get("due") is None, t.get("due") or "", t["id"]))
    assert result[0]["title"] == "Today"
    assert result[1]["title"] == "Tomorrow"
    assert result[2]["title"] == "No date"
