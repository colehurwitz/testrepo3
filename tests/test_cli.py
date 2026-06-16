import sys
import pytest
from todo.cli import main
import todo.store


@pytest.fixture
def tmp_store(tmp_path, monkeypatch):
    store_path = tmp_path / "todos.json"
    monkeypatch.setattr(todo.store, "DEFAULT_PATH", store_path)
    return store_path


def test_version_flag(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "--version"])
    main()
    captured = capsys.readouterr()
    assert "todo-cli" in captured.out
    assert "0.1.0" in captured.out


def test_no_args(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo"])
    ret = main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert ret == 0


def test_unknown_command(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "bogus"])
    ret = main()
    captured = capsys.readouterr()
    assert "Unknown command: bogus" in captured.out
    assert ret == 1


def test_list_empty(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    assert "No todos yet" in captured.out


def test_add_and_list(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy milk"])
    main()
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    assert "Buy milk" in captured.out

    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    assert "Buy milk" in captured.out
    assert "[ ]" in captured.out


def test_add_missing_title(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add"])
    ret = main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert ret == 1


def test_done_happy(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Task"])
    main()
    monkeypatch.setattr(sys, "argv", ["todo", "done", "1"])
    ret = main()
    captured = capsys.readouterr()
    assert "Completed: Task" in captured.out
    assert ret == 0


def test_done_not_found(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "done", "99"])
    ret = main()
    captured = capsys.readouterr()
    assert "not found" in captured.out
    assert ret == 1


def test_done_invalid_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "done", "abc"])
    ret = main()
    captured = capsys.readouterr()
    assert "not a valid todo ID" in captured.out
    assert ret == 1


def test_done_missing_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "done"])
    ret = main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert ret == 1


def test_delete_happy(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Trash"])
    main()
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "1"])
    ret = main()
    captured = capsys.readouterr()
    assert "Deleted todo 1" in captured.out
    assert ret == 0


def test_delete_not_found(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "99"])
    ret = main()
    captured = capsys.readouterr()
    assert "not found" in captured.out
    assert ret == 1


def test_delete_invalid_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "delete", "abc"])
    ret = main()
    captured = capsys.readouterr()
    assert "not a valid todo ID" in captured.out
    assert ret == 1


def test_delete_missing_id(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "delete"])
    ret = main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert ret == 1


def test_add_with_due_date(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Deadline task", "--due", "2026-06-20"])
    ret = main()
    captured = capsys.readouterr()
    assert "Added:" in captured.out
    assert ret == 0

    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    assert "(due: 2026-06-20)" in captured.out


def test_add_without_due_date(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "No deadline"])
    main()
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    assert "(due:" not in captured.out


def test_add_invalid_due_date(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Bad date", "--due", "not-a-date"])
    ret = main()
    captured = capsys.readouterr()
    assert "not a valid date" in captured.out
    assert ret == 1


def test_add_due_missing_value(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Oops", "--due"])
    ret = main()
    captured = capsys.readouterr()
    assert "--due requires a date" in captured.out
    assert ret == 1


def test_list_sort_due(capsys, monkeypatch, tmp_store):
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Later", "--due", "2026-12-01"])
    main()
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Sooner", "--due", "2026-06-01"])
    main()
    monkeypatch.setattr(sys, "argv", ["todo", "add", "No date"])
    main()
    capsys.readouterr()

    monkeypatch.setattr(sys, "argv", ["todo", "list", "--sort", "due"])
    main()
    captured = capsys.readouterr()
    lines = [l for l in captured.out.strip().split("\n") if l.strip()]
    assert "Sooner" in lines[0]
    assert "Later" in lines[1]
    assert "No date" in lines[2]


def test_corrupted_json(capsys, monkeypatch, tmp_store):
    tmp_store.write_text("{invalid json")
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    main()
    captured = capsys.readouterr()
    assert "Warning: corrupted JSON" in captured.out
    assert "No todos yet" in captured.out
