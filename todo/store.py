import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".todo.json"


def load_todos(path: Path = DEFAULT_PATH) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_todos(todos: list[dict], path: Path = DEFAULT_PATH) -> None:
    path.write_text(json.dumps(todos))


VALID_PRIORITIES = ("high", "medium", "low")


def add_todo(title: str, path: Path = DEFAULT_PATH, priority: str = "medium") -> dict:
    todos = load_todos(path)
    todo = {"id": len(todos) + 1, "title": title, "done": False, "priority": priority}
    todos.append(todo)
    save_todos(todos, path)
    return todo


def complete_todo(todo_id: int, path: Path = DEFAULT_PATH) -> dict | None:
    todos = load_todos(path)
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos, path)
            return t
    return None


def delete_todo(todo_id: int, path: Path = DEFAULT_PATH) -> bool:
    todos = load_todos(path)
    new = [t for t in todos if t["id"] != todo_id]
    if len(new) == len(todos):
        return False
    save_todos(new, path)
    return True


def search_todos(query: str, path: Path = DEFAULT_PATH) -> list[dict]:
    todos = load_todos(path)
    return [t for t in todos if query.lower() in t["title"].lower()]
