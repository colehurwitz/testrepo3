import json
from datetime import date
from pathlib import Path

DEFAULT_PATH = Path.home() / ".todo.json"


def load_todos(path: Path = DEFAULT_PATH) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_todos(todos: list[dict], path: Path = DEFAULT_PATH) -> None:
    path.write_text(json.dumps(todos))


def parse_due_date(date_str: str) -> str:
    try:
        return date.fromisoformat(date_str).isoformat()
    except ValueError:
        raise ValueError(f"Invalid date: '{date_str}'. Use YYYY-MM-DD format.")


def add_todo(title: str, due: str | None = None, path: Path = DEFAULT_PATH) -> dict:
    if due is not None:
        due = parse_due_date(due)
    todos = load_todos(path)
    todo = {"id": len(todos) + 1, "title": title, "done": False, "due": due}
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
