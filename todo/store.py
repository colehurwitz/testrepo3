import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".todo.json"


def load_todos(path: Path | None = None) -> list[dict]:
    path = path or DEFAULT_PATH
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        print(f"Warning: corrupted JSON in {path}, starting fresh")
        return []


def save_todos(todos: list[dict], path: Path | None = None) -> None:
    path = path or DEFAULT_PATH
    path.write_text(json.dumps(todos, indent=2))


def add_todo(title: str, path: Path | None = None, due: str | None = None) -> dict:
    path = path or DEFAULT_PATH
    todos = load_todos(path)
    next_id = max((t["id"] for t in todos), default=0) + 1
    todo = {"id": next_id, "title": title, "done": False, "due": due}
    todos.append(todo)
    save_todos(todos, path)
    return todo


def complete_todo(todo_id: int, path: Path | None = None) -> dict | None:
    path = path or DEFAULT_PATH
    todos = load_todos(path)
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos, path)
            return t
    return None


def delete_todo(todo_id: int, path: Path | None = None) -> bool:
    path = path or DEFAULT_PATH
    todos = load_todos(path)
    new = [t for t in todos if t["id"] != todo_id]
    if len(new) == len(todos):
        return False
    save_todos(new, path)
    return True
