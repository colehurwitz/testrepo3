import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".todo.json"


def load_todos(path: Path | None = None) -> list[dict]:
    if path is None:
        path = DEFAULT_PATH
    if not path.exists():
        return []
    todos = json.loads(path.read_text())
    for todo in todos:
        todo.setdefault("priority", "medium")
    return todos


def save_todos(todos: list[dict], path: Path | None = None) -> None:
    if path is None:
        path = DEFAULT_PATH
    path.write_text(json.dumps(todos))


def add_todo(title: str, priority: str = "medium", path: Path | None = None) -> dict:
    if path is None:
        path = DEFAULT_PATH
    todos = load_todos(path)
    todo = {"id": len(todos) + 1, "title": title, "done": False, "priority": priority}
    todos.append(todo)
    save_todos(todos, path)
    return todo


def complete_todo(todo_id: int, path: Path | None = None) -> dict | None:
    if path is None:
        path = DEFAULT_PATH
    todos = load_todos(path)
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos, path)
            return t
    return None


def delete_todo(todo_id: int, path: Path | None = None) -> bool:
    if path is None:
        path = DEFAULT_PATH
    todos = load_todos(path)
    new = [t for t in todos if t["id"] != todo_id]
    if len(new) == len(todos):
        return False
    save_todos(new, path)
    return True
