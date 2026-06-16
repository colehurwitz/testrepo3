import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".todo.json"


def _resolve_path(path: Path | None) -> Path:
    if path is None:
        return DEFAULT_PATH
    return path


def load_todos(path: Path | None = None) -> list[dict]:
    path = _resolve_path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_todos(todos: list[dict], path: Path | None = None) -> None:
    path = _resolve_path(path)
    path.write_text(json.dumps(todos))


def add_todo(title: str, priority: str = "medium", due: str | None = None,
             path: Path | None = None) -> dict:
    valid_priorities = {"high", "medium", "low"}
    if priority not in valid_priorities:
        raise ValueError(f"Invalid priority '{priority}'. Must be one of: high, medium, low")
    if due is not None:
        import datetime
        try:
            datetime.date.fromisoformat(due)
        except ValueError:
            raise ValueError(f"Invalid date '{due}'. Must be YYYY-MM-DD format")
    path = _resolve_path(path)
    todos = load_todos(path)
    next_id = max((t["id"] for t in todos), default=0) + 1
    todo = {"id": next_id, "title": title, "done": False, "priority": priority, "due": due}
    todos.append(todo)
    save_todos(todos, path)
    return todo


def complete_todo(todo_id: int, path: Path | None = None) -> dict | None:
    path = _resolve_path(path)
    todos = load_todos(path)
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos, path)
            return t
    return None


def delete_todo(todo_id: int, path: Path | None = None) -> bool:
    path = _resolve_path(path)
    todos = load_todos(path)
    new = [t for t in todos if t["id"] != todo_id]
    if len(new) == len(todos):
        return False
    save_todos(new, path)
    return True


def search_todos(query: str, status_filter: str | None = None,
                 path: Path | None = None) -> list[dict]:
    path = _resolve_path(path)
    todos = load_todos(path)
    results = [t for t in todos if query.lower() in t["title"].lower()]
    if status_filter == "done":
        results = [t for t in results if t["done"]]
    elif status_filter == "pending":
        results = [t for t in results if not t["done"]]
    return results
