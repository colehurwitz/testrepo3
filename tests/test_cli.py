import sys
from todo.cli import main
from todo.store import add_todo, complete_todo


def test_version_flag(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "--version"])
    main()
    captured = capsys.readouterr()
    assert "todo-cli" in captured.out
    assert "0.1.0" in captured.out


def test_search_command(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    add_todo("Buy milk", store)
    add_todo("Walk dog", store)
    monkeypatch.setattr(sys, "argv", ["todo", "search", "buy"])
    monkeypatch.setattr("todo.cli.search_todos", lambda q: __import__("todo.store", fromlist=["search_todos"]).search_todos(q, store))
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
    monkeypatch.setattr("todo.cli.search_todos", lambda q: __import__("todo.store", fromlist=["search_todos"]).search_todos(q, store))
    main()
    captured = capsys.readouterr()
    assert "Buy milk" in captured.out
    assert "Buy eggs" not in captured.out


def test_add_with_priority(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Urgent task", "--priority", "high"])
    monkeypatch.setattr("todo.cli.add_todo", lambda title, priority="medium": add_todo(title, store, priority=priority))
    main()
    captured = capsys.readouterr()
    assert "Urgent task" in captured.out
    assert "(high)" in captured.out


def test_add_default_priority(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Normal task"])
    monkeypatch.setattr("todo.cli.add_todo", lambda title, priority="medium": add_todo(title, store, priority=priority))
    main()
    captured = capsys.readouterr()
    assert "Normal task" in captured.out
    assert "(medium)" in captured.out


def test_add_invalid_priority(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Bad task", "--priority", "urgent"])
    main()
    captured = capsys.readouterr()
    assert "Invalid priority" in captured.out


def test_list_with_priority_filter(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    add_todo("High task", store, priority="high")
    add_todo("Low task", store, priority="low")
    add_todo("Med task", store, priority="medium")
    monkeypatch.setattr(sys, "argv", ["todo", "list", "--priority", "high"])
    monkeypatch.setattr("todo.cli.load_todos", lambda: __import__("todo.store", fromlist=["load_todos"]).load_todos(store))
    main()
    captured = capsys.readouterr()
    assert "High task" in captured.out
    assert "Low task" not in captured.out
    assert "Med task" not in captured.out


def test_list_shows_priority(capsys, monkeypatch, tmp_path):
    store = tmp_path / "todos.json"
    add_todo("Task one", store, priority="high")
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    monkeypatch.setattr("todo.cli.load_todos", lambda: __import__("todo.store", fromlist=["load_todos"]).load_todos(store))
    main()
    captured = capsys.readouterr()
    assert "(high)" in captured.out
