import pytest
from pathlib import Path
from todo.store import add_todo, load_todos, complete_todo, delete_todo


@pytest.fixture
def tmp_store(tmp_path):
    return tmp_path / "todos.json"


def test_add_and_load(tmp_store):
    add_todo("Buy milk", tmp_store)
    add_todo("Walk dog", tmp_store)
    todos = load_todos(tmp_store)
    assert len(todos) == 2
    assert todos[0]["title"] == "Buy milk"
    assert todos[1]["title"] == "Walk dog"


def test_complete(tmp_store):
    add_todo("Read book", tmp_store)
    result = complete_todo(1, tmp_store)
    assert result is not None
    assert result["done"] is True


def test_complete_missing(tmp_store):
    result = complete_todo(99, tmp_store)
    assert result is None


def test_delete(tmp_store):
    add_todo("Trash", tmp_store)
    assert delete_todo(1, tmp_store) is True
    assert load_todos(tmp_store) == []


def test_delete_missing(tmp_store):
    assert delete_todo(99, tmp_store) is False


def test_id_no_collision_after_delete(tmp_store):
    add_todo("A", tmp_store)
    add_todo("B", tmp_store)
    add_todo("C", tmp_store)
    delete_todo(2, tmp_store)
    new = add_todo("D", tmp_store)
    todos = load_todos(tmp_store)
    ids = [t["id"] for t in todos]
    assert new["id"] not in [1, 3] or new["id"] == 4
    assert len(ids) == len(set(ids))
