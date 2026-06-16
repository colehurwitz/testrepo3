import sys
import datetime
from todo import __version__
from todo.store import add_todo, load_todos, complete_todo, delete_todo
from pathlib import Path


def print_todos(todos: list[dict]) -> None:
    if not todos:
        print("No todos yet. Add one with: todo add <title>")
        return
    for t in todos:
        status = "x" if t["done"] else " "
        due_str = f" (due: {t['due']})" if t.get("due") else ""
        print(f"  [{status}] {t['id']}: {t['title']}{due_str}")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("Usage: todo <command> [args]")
        print("Commands: list, add, done, delete")
        print("Options: --version")
        return 0

    if "--version" in args:
        print(f"todo-cli {__version__}")
        return 0

    cmd = args[0]

    if cmd == "list":
        todos = load_todos()
        if "--sort" in args:
            sort_idx = args.index("--sort")
            if sort_idx + 1 < len(args) and args[sort_idx + 1] == "due":
                todos.sort(key=lambda t: (t.get("due") is None, t.get("due") or ""))
        print_todos(todos)

    elif cmd == "add":
        if len(args) < 2:
            print("Usage: todo add <title> [--due YYYY-MM-DD]")
            return 1
        due = None
        title_parts = []
        i = 1
        while i < len(args):
            if args[i] == "--due":
                if i + 1 >= len(args):
                    print("Error: --due requires a date argument (YYYY-MM-DD)")
                    return 1
                try:
                    datetime.date.fromisoformat(args[i + 1])
                    due = args[i + 1]
                except ValueError:
                    print(f"Error: '{args[i + 1]}' is not a valid date (use YYYY-MM-DD)")
                    return 1
                i += 2
            else:
                title_parts.append(args[i])
                i += 1
        if not title_parts:
            print("Usage: todo add <title> [--due YYYY-MM-DD]")
            return 1
        title = " ".join(title_parts)
        todo = add_todo(title, due=due)
        print(f"Added: [{todo['id']}] {todo['title']}")

    elif cmd == "done":
        if len(args) < 2:
            print("Usage: todo done <id>")
            return 1
        try:
            todo_id = int(args[1])
        except ValueError:
            print(f"Error: '{args[1]}' is not a valid todo ID")
            return 1
        result = complete_todo(todo_id)
        if result:
            print(f"Completed: {result['title']}")
        else:
            print(f"Todo {todo_id} not found")
            return 1

    elif cmd == "delete":
        if len(args) < 2:
            print("Usage: todo delete <id>")
            return 1
        try:
            todo_id = int(args[1])
        except ValueError:
            print(f"Error: '{args[1]}' is not a valid todo ID")
            return 1
        if delete_todo(todo_id):
            print(f"Deleted todo {todo_id}")
        else:
            print(f"Todo {todo_id} not found")
            return 1

    else:
        print(f"Unknown command: {cmd}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
