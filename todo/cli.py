import sys
from todo.store import add_todo, load_todos, complete_todo, delete_todo
from pathlib import Path


def print_todos(todos: list[dict]) -> None:
    if not todos:
        print("No todos yet. Add one with: todo add <title>")
        return
    todos = sorted(todos, key=lambda t: (t.get("due") is None, t.get("due") or "", t["id"]))
    for t in todos:
        status = "x" if t["done"] else " "
        due = f" (due: {t['due']})" if t.get("due") else ""
        print(f"  [{status}] {t['id']}: {t['title']}{due}")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: todo <command> [args]")
        print("Commands: list, add, done, delete")
        return

    cmd = args[0]

    if cmd == "list":
        todos = load_todos()
        print_todos(todos)

    elif cmd == "add":
        if len(args) < 2:
            print("Usage: todo add <title> [--due YYYY-MM-DD]")
            return
        remaining = list(args[1:])
        due = None
        if "--due" in remaining:
            idx = remaining.index("--due")
            if idx + 1 >= len(remaining):
                print("Error: --due requires a date (YYYY-MM-DD)")
                return
            due = remaining[idx + 1]
            del remaining[idx:idx + 2]
        if not remaining:
            print("Usage: todo add <title> [--due YYYY-MM-DD]")
            return
        title = " ".join(remaining)
        try:
            todo = add_todo(title, due=due)
        except ValueError as e:
            print(str(e))
            return
        due_str = f" (due: {todo['due']})" if todo.get("due") else ""
        print(f"Added: [{todo['id']}] {todo['title']}{due_str}")

    elif cmd == "done":
        if len(args) < 2:
            print("Usage: todo done <id>")
            return
        todo_id = int(args[1])
        result = complete_todo(todo_id)
        if result:
            print(f"Completed: {result['title']}")
        else:
            print(f"Todo {todo_id} not found")

    elif cmd == "delete":
        if len(args) < 2:
            print("Usage: todo delete <id>")
            return
        todo_id = int(args[1])
        if delete_todo(todo_id):
            print(f"Deleted todo {todo_id}")
        else:
            print(f"Todo {todo_id} not found")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
