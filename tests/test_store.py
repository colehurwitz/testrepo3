import pytest
import os
import stat
from todo.store import add_todo, load_todos, save_todos, complete_todo, delete_todo, search_todos


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


def test_search_matches(tmp_store):
    add_todo("Buy milk", tmp_store)
    add_todo("Buy eggs", tmp_store)
    add_todo("Walk dog", tmp_store)
    results = search_todos("buy", tmp_store)
    assert len(results) == 2
    assert {r["title"] for r in results} == {"Buy milk", "Buy eggs"}


def test_search_case_insensitive(tmp_store):
    add_todo("Buy Milk", tmp_store)
    results = search_todos("buy milk", tmp_store)
    assert len(results) == 1
    assert results[0]["title"] == "Buy Milk"


def test_search_no_results(tmp_store):
    add_todo("Buy milk", tmp_store)
    assert search_todos("xyz", tmp_store) == []


skip_if_root = pytest.mark.skipif(
    os.geteuid() == 0, reason="root bypasses file permissions"
)


@skip_if_root
def test_load_permission_denied(tmp_store):
    """load_todos raises PermissionError when file is not readable."""
    tmp_store.write_text("[]")
    os.chmod(tmp_store, 0o000)
    try:
        with pytest.raises(PermissionError):
            load_todos(tmp_store)
    finally:
        os.chmod(tmp_store, stat.S_IRUSR | stat.S_IWUSR)


@skip_if_root
def test_save_permission_denied(tmp_store):
    """save_todos raises PermissionError when file is not writable."""
    tmp_store.write_text("[]")
    os.chmod(tmp_store, stat.S_IRUSR)  # Read-only
    try:
        with pytest.raises(PermissionError):
            save_todos([], tmp_store)
    finally:
        os.chmod(tmp_store, stat.S_IRUSR | stat.S_IWUSR)


@skip_if_root
def test_add_permission_denied(tmp_store):
    """add_todo raises PermissionError when file is not writable."""
    tmp_store.write_text("[]")
    os.chmod(tmp_store, stat.S_IRUSR)  # Read-only
    try:
        with pytest.raises(PermissionError):
            add_todo("Test", tmp_store)
    finally:
        os.chmod(tmp_store, stat.S_IRUSR | stat.S_IWUSR)


@skip_if_root
def test_add_unwritable_directory(tmp_path):
    """add_todo raises PermissionError when directory is not writable."""
    subdir = tmp_path / "locked"
    subdir.mkdir()
    store = subdir / "todos.json"
    os.chmod(subdir, stat.S_IRUSR | stat.S_IXUSR)  # Read+execute only
    try:
        with pytest.raises(PermissionError):
            add_todo("Test", store)
    finally:
        os.chmod(subdir, stat.S_IRWXU)
