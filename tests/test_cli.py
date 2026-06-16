import sys
import pytest
from todo.cli import main


@pytest.fixture
def tmp_store(tmp_path):
    return tmp_path / "todos.json"


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
    assert "list" in captured.out


def test_unknown_command(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "bogus"])
    main()
    captured = capsys.readouterr()
    assert "Unknown command: bogus" in captured.out


def test_add_todo(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy milk"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    assert "Buy milk" in captured.out


def test_add_missing_title(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Usage: todo add" in captured.out


def test_list_empty(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "No todos yet" in captured.out


def test_list_with_todos(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Task one"])
    main(path=tmp_store)
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Task one" in captured.out
    assert "[ ]" in captured.out


def test_done_valid_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Finish report"])
    main(path=tmp_store)
    monkeypatch.setattr(sys, "argv", ["todo", "done", "1"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Completed: Finish report" in captured.out


def test_done_not_found(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "done", "99"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_done_invalid_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "done", "abc"])
    with pytest.raises(SystemExit, match="1"):
        main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Error: 'abc' is not a valid todo ID" in captured.err


def test_done_missing_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "done"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Usage: todo done" in captured.out


def test_delete_valid_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Trash"])
    main(path=tmp_store)
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "1"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Deleted todo 1" in captured.out


def test_delete_not_found(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "99"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_delete_invalid_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "abc"])
    with pytest.raises(SystemExit, match="1"):
        main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Error: 'abc' is not a valid todo ID" in captured.err


def test_delete_missing_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "delete"])
    main(path=tmp_store)
    captured = capsys.readouterr()
    assert "Usage: todo delete" in captured.out
