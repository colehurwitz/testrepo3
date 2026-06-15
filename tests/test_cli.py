import pytest
from unittest.mock import patch
from todo.cli import main
from todo.store import load_todos


@pytest.fixture
def tmp_store(tmp_path):
    return tmp_path / "todos.json"


@pytest.fixture(autouse=True)
def use_tmp_store(tmp_store):
    with patch("todo.store.DEFAULT_PATH", tmp_store):
        yield


def test_add_with_priority_flag(tmp_store, capsys):
    main(["add", "Test", "--priority", "high"])
    todos = load_todos(tmp_store)
    assert len(todos) == 1
    assert todos[0]["priority"] == "high"


def test_add_default_priority(tmp_store, capsys):
    main(["add", "Test"])
    todos = load_todos(tmp_store)
    assert todos[0]["priority"] == "medium"


def test_list_shows_priority(capsys):
    main(["add", "High task", "-p", "high"])
    main(["add", "Low task", "-p", "low"])
    main(["list"])
    output = capsys.readouterr().out
    assert "[H]" in output
    assert "[L]" in output


def test_list_filter_by_priority(capsys):
    main(["add", "High task", "-p", "high"])
    main(["add", "Medium task"])
    main(["add", "Low task", "-p", "low"])
    capsys.readouterr()
    main(["list", "--priority", "high"])
    output = capsys.readouterr().out
    assert "High task" in output
    assert "Medium task" not in output
    assert "Low task" not in output


def test_add_invalid_priority():
    with pytest.raises(SystemExit) as exc_info:
        main(["add", "Test", "--priority", "urgent"])
    assert exc_info.value.code == 2
