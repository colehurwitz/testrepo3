import sys
from todo import __version__
from todo.cli import main
from todo.store import add_todo, complete_todo


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


def test_done_invalid_id(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "done", "abc"])
    main()
    captured = capsys.readouterr()
    assert "Error: 'abc' is not a valid todo ID. Please provide a number." in captured.out


def test_delete_invalid_id(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "xyz"])
    main()
    captured = capsys.readouterr()
    assert "Error: 'xyz' is not a valid todo ID. Please provide a number." in captured.out
