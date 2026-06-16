import pytest
from pathlib import Path
from todo.store import add_todo, load_todos, complete_todo, delete_todo, search_todos


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


# --- ID collision regression tests (Issue #2) ---

def test_id_no_collision_after_delete(tmp_store):
    add_todo("First", path=tmp_store)
    add_todo("Second", path=tmp_store)
    add_todo("Third", path=tmp_store)
    delete_todo(2, tmp_store)
    new = add_todo("Fourth", path=tmp_store)
    assert new["id"] == 4


def test_id_after_delete_all(tmp_store):
    add_todo("Only", path=tmp_store)
    delete_todo(1, tmp_store)
    new = add_todo("New", path=tmp_store)
    assert new["id"] == 1  # no collision possible when list is empty


def test_ids_unique_across_cycles(tmp_store):
    for i in range(5):
        add_todo(f"Task {i}", path=tmp_store)
    delete_todo(2, tmp_store)
    delete_todo(4, tmp_store)
    new1 = add_todo("New1", path=tmp_store)
    new2 = add_todo("New2", path=tmp_store)
    assert new1["id"] == 6
    assert new2["id"] == 7
    todos = load_todos(tmp_store)
    ids = [t["id"] for t in todos]
    assert len(ids) == len(set(ids))


# --- Priority tests (Issue #4) ---

def test_add_with_priority(tmp_store):
    todo = add_todo("Important task", priority="high", path=tmp_store)
    assert todo["priority"] == "high"


def test_add_default_priority(tmp_store):
    todo = add_todo("Normal task", path=tmp_store)
    assert todo["priority"] == "medium"


def test_add_invalid_priority(tmp_store):
    with pytest.raises(ValueError, match="Invalid priority"):
        add_todo("Bad task", priority="critical", path=tmp_store)


# --- Due date tests (Issue #3) ---

def test_add_with_due_date(tmp_store):
    todo = add_todo("Deadline task", due="2025-06-01", path=tmp_store)
    assert todo["due"] == "2025-06-01"


def test_add_default_no_due(tmp_store):
    todo = add_todo("No deadline", path=tmp_store)
    assert todo["due"] is None


def test_add_invalid_due_date(tmp_store):
    with pytest.raises(ValueError, match="Invalid date"):
        add_todo("Bad date", due="not-a-date", path=tmp_store)


def test_add_invalid_due_date_format(tmp_store):
    with pytest.raises(ValueError, match="Invalid date"):
        add_todo("Bad format", due="13/01/2025", path=tmp_store)


def test_backward_compat_old_todos(tmp_store):
    import json
    old_todos = [{"id": 1, "title": "Old todo", "done": False}]
    tmp_store.write_text(json.dumps(old_todos))
    todos = load_todos(tmp_store)
    assert todos[0]["title"] == "Old todo"
    assert todos[0].get("priority") is None
    assert todos[0].get("due") is None


# --- Search tests (Issue #5) ---

def test_search_matches(tmp_store):
    add_todo("Buy milk", path=tmp_store)
    add_todo("Buy eggs", path=tmp_store)
    add_todo("Walk dog", path=tmp_store)
    results = search_todos("buy", path=tmp_store)
    assert len(results) == 2


def test_search_no_matches(tmp_store):
    add_todo("Buy milk", path=tmp_store)
    results = search_todos("xyz", path=tmp_store)
    assert len(results) == 0


def test_search_case_insensitive(tmp_store):
    add_todo("Buy MILK", path=tmp_store)
    results = search_todos("milk", path=tmp_store)
    assert len(results) == 1


def test_search_done_filter(tmp_store):
    add_todo("Task A", path=tmp_store)
    add_todo("Task B", path=tmp_store)
    complete_todo(1, tmp_store)
    results = search_todos("Task", status_filter="done", path=tmp_store)
    assert len(results) == 1
    assert results[0]["title"] == "Task A"


def test_search_pending_filter(tmp_store):
    add_todo("Task A", path=tmp_store)
    add_todo("Task B", path=tmp_store)
    complete_todo(1, tmp_store)
    results = search_todos("Task", status_filter="pending", path=tmp_store)
    assert len(results) == 1
    assert results[0]["title"] == "Task B"
