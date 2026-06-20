import sys
from todo import __version__
from todo.cli import main, parse_date
from todo.store import add_todo, complete_todo, load_todos
import pytest


def test_version_flag(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "--version"])
    main()
    captured = capsys.readouterr()
    assert "todo-cli" in captured.out
    assert __version__ in captured.out


def test_version_short_flag(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "-V"])
    main()
    captured = capsys.readouterr()
    assert "todo-cli" in captured.out
    assert __version__ in captured.out


def test_search_command(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    add_todo("Buy milk", store)
    add_todo("Walk dog", store)
    monkeypatch.setattr(sys, "argv", ["todo", "search", "buy"])
    monkeypatch.setattr(
        "todo.cli.search_todos",
        lambda q: __import__("todo.store", fromlist=["search_todos"]).search_todos(
            q, store
        ),
    )
    main()
    captured = capsys.readouterr()
    assert "Buy milk" in captured.out
    assert "Walk dog" not in captured.out


def test_search_no_args(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "search"])
    main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_search_with_done_flag(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    add_todo("Buy milk", store)
    add_todo("Buy eggs", store)
    complete_todo(1, store)
    monkeypatch.setattr(sys, "argv", ["todo", "search", "buy", "--done"])
    monkeypatch.setattr(
        "todo.cli.search_todos",
        lambda q: __import__("todo.store", fromlist=["search_todos"]).search_todos(
            q, store
        ),
    )
    main()
    captured = capsys.readouterr()
    assert "Buy milk" in captured.out
    assert "Buy eggs" not in captured.out


def test_parse_date_valid():
    assert parse_date("2025-01-15") == "2025-01-15"
    assert parse_date("2024-12-31") == "2024-12-31"


def test_parse_date_invalid():
    with pytest.raises(ValueError) as exc_info:
        parse_date("invalid-date")
    assert "Invalid date format" in str(exc_info.value)
    assert "YYYY-MM-DD" in str(exc_info.value)


def test_parse_date_invalid_format():
    with pytest.raises(ValueError) as exc_info:
        parse_date("01-15-2025")
    assert "Invalid date format" in str(exc_info.value)


def test_add_with_due_date(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy milk", "--due", "2025-01-15"])
    monkeypatch.setattr(
        "todo.cli.add_todo",
        lambda title, due=None: __import__("todo.store", fromlist=["add_todo"]).add_todo(
            title, store, due=due
        ),
    )
    main()
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    assert "Buy milk" in captured.out
    assert "(due: 2025-01-15)" in captured.out
    todos = load_todos(store)
    assert todos[0]["due"] == "2025-01-15"


def test_add_without_due_date(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy milk"])
    monkeypatch.setattr(
        "todo.cli.add_todo",
        lambda title, due=None: __import__("todo.store", fromlist=["add_todo"]).add_todo(
            title, store, due=due
        ),
    )
    main()
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    assert "Buy milk" in captured.out
    assert "(due:" not in captured.out


def test_add_with_invalid_due_date(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy milk", "--due", "invalid"])
    main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "Invalid date format" in captured.out


def test_add_with_due_missing_arg(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy milk", "--due"])
    main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "--due requires a date argument" in captured.out


def test_list_shows_due_dates(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    add_todo("Buy milk", store, due="2025-01-15")
    add_todo("Walk dog", store)
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    monkeypatch.setattr(
        "todo.cli.load_todos",
        lambda: __import__("todo.store", fromlist=["load_todos"]).load_todos(store),
    )
    main()
    captured = capsys.readouterr()
    assert "Buy milk (due: 2025-01-15)" in captured.out
    assert "Walk dog" in captured.out
    assert "Walk dog (due:" not in captured.out


def test_list_sorts_by_due_date(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    add_todo("No due date", store)
    add_todo("Later", store, due="2025-03-01")
    add_todo("Sooner", store, due="2025-01-15")
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    monkeypatch.setattr(
        "todo.cli.load_todos",
        lambda: __import__("todo.store", fromlist=["load_todos"]).load_todos(store),
    )
    main()
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert "Sooner" in lines[0]
    assert "Later" in lines[1]
    assert "No due date" in lines[2]
