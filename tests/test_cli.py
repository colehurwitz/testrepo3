import sys
import json
import pytest
from todo.cli import main


def test_version_flag(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "--version"])
    main()
    captured = capsys.readouterr()
    assert "todo-cli" in captured.out
    assert "0.1.0" in captured.out


def test_no_args(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo"])
    main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_unknown_command(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "foobar"])
    main()
    captured = capsys.readouterr()
    assert "Unknown command: foobar" in captured.out


# --- Input validation tests (Issue #1) ---

def test_done_non_integer(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "done", "abc"])
    main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "not a valid todo ID" in captured.out


def test_delete_non_integer(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "abc"])
    main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "not a valid todo ID" in captured.out


def test_done_missing_arg(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "done"])
    main()
    captured = capsys.readouterr()
    assert "Usage: todo done <id>" in captured.out


def test_delete_missing_arg(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "delete"])
    main()
    captured = capsys.readouterr()
    assert "Usage: todo delete <id>" in captured.out


# --- Add command tests ---

def test_add_missing_title(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "add"])
    main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_add_todo(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy", "milk"])
    main()
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    assert "Buy milk" in captured.out


def test_add_with_priority(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Urgent", "task", "--priority", "high"])
    main()
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    todos = json.loads(store.read_text())
    assert todos[0]["priority"] == "high"


def test_add_with_due(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Deadline", "task", "--due", "2025-06-01"])
    main()
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    todos = json.loads(store.read_text())
    assert todos[0]["due"] == "2025-06-01"


def test_add_invalid_priority(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Task", "--priority", "critical"])
    main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out


def test_add_invalid_due(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Task", "--due", "not-a-date"])
    main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out


# --- List command tests ---

def test_list_empty(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    assert "No todos yet" in captured.out


def test_list_with_priority_filter(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    from todo.store import add_todo
    add_todo("High task", priority="high", path=store)
    add_todo("Low task", priority="low", path=store)
    monkeypatch.setattr(sys, "argv", ["todo", "list", "--priority", "high"])
    main()
    captured = capsys.readouterr()
    assert "High task" in captured.out
    assert "Low task" not in captured.out


def test_list_sorted_by_due(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    from todo.store import add_todo
    add_todo("Later", due="2025-12-01", path=store)
    add_todo("Sooner", due="2025-01-01", path=store)
    add_todo("No date", path=store)
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    lines = [l for l in captured.out.strip().split("\n") if l.strip()]
    assert "Sooner" in lines[0]
    assert "Later" in lines[1]
    assert "No date" in lines[2]


# --- Done/Delete with valid IDs ---

def test_done_valid(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    from todo.store import add_todo
    add_todo("Task", path=store)
    monkeypatch.setattr(sys, "argv", ["todo", "done", "1"])
    main()
    captured = capsys.readouterr()
    assert "Completed:" in captured.out


def test_delete_valid(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    from todo.store import add_todo
    add_todo("Task", path=store)
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "1"])
    main()
    captured = capsys.readouterr()
    assert "Deleted todo 1" in captured.out


def test_done_not_found(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    monkeypatch.setattr(sys, "argv", ["todo", "done", "99"])
    main()
    captured = capsys.readouterr()
    assert "not found" in captured.out


# --- Search command tests (Issue #5) ---

def test_search_missing_query(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "search"])
    main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_search_results(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    from todo.store import add_todo
    add_todo("Buy milk", path=store)
    add_todo("Buy eggs", path=store)
    add_todo("Walk dog", path=store)
    monkeypatch.setattr(sys, "argv", ["todo", "search", "buy"])
    main()
    captured = capsys.readouterr()
    assert "Buy milk" in captured.out
    assert "Buy eggs" in captured.out
    assert "Walk dog" not in captured.out


def test_search_with_done_filter(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    from todo.store import add_todo, complete_todo
    add_todo("Task A", path=store)
    add_todo("Task B", path=store)
    complete_todo(1, store)
    monkeypatch.setattr(sys, "argv", ["todo", "search", "Task", "--done"])
    main()
    captured = capsys.readouterr()
    assert "Task A" in captured.out
    assert "Task B" not in captured.out


def test_search_with_pending_filter(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr("todo.store.DEFAULT_PATH", store)
    from todo.store import add_todo, complete_todo
    add_todo("Task A", path=store)
    add_todo("Task B", path=store)
    complete_todo(1, store)
    monkeypatch.setattr(sys, "argv", ["todo", "search", "Task", "--pending"])
    main()
    captured = capsys.readouterr()
    assert "Task B" in captured.out
    assert "Task A" not in captured.out
