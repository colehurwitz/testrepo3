import sys
from datetime import date
from todo import __version__
from todo.store import add_todo, load_todos, complete_todo, delete_todo, search_todos


def parse_date(date_str: str) -> str:
    """Parse and validate a date string in YYYY-MM-DD format."""
    try:
        date.fromisoformat(date_str)
        return date_str
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD format.")


def print_todos(todos: list[dict]) -> None:
    if not todos:
        print("No todos yet. Add one with: todo add <title>")
        return
    for t in todos:
        status = "x" if t["done"] else " "
        due_str = f" (due: {t['due']})" if t.get("due") else ""
        print(f"  [{status}] {t['id']}: {t['title']}{due_str}")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: todo <command> [args]")
        print("Commands: list, add, done, delete, search")
        print("Options: --version, -V")
        return

    if "--version" in args or "-V" in args:
        print(f"todo-cli {__version__}")
        return

    cmd = args[0]

    if cmd == "list":
        todos = load_todos()
        todos = sorted(todos, key=lambda t: (t.get('due') is None, t.get('due') or ''))
        print_todos(todos)

    elif cmd == "add":
        if len(args) < 2:
            print("Usage: todo add <title> [--due YYYY-MM-DD]")
            return
        due = None
        title_parts = []
        i = 1
        while i < len(args):
            if args[i] == "--due":
                if i + 1 >= len(args):
                    print("Error: --due requires a date argument")
                    return
                try:
                    due = parse_date(args[i + 1])
                except ValueError as e:
                    print(f"Error: {e}")
                    return
                i += 2
            else:
                title_parts.append(args[i])
                i += 1
        if not title_parts:
            print("Usage: todo add <title> [--due YYYY-MM-DD]")
            return
        title = " ".join(title_parts)
        todo = add_todo(title, due=due)
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

    elif cmd == "search":
        if len(args) < 2:
            print("Usage: todo search <query> [--done | --pending]")
            return
        flag_done = "--done" in args[1:]
        flag_pending = "--pending" in args[1:]
        query = " ".join(a for a in args[1:] if a not in ("--done", "--pending"))
        results = search_todos(query)
        if flag_done and not flag_pending:
            results = [t for t in results if t["done"]]
        elif flag_pending and not flag_done:
            results = [t for t in results if not t["done"]]
        if not results:
            print("No matching todos found.")
            return
        print_todos(results)

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
