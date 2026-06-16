import sys
from todo import __version__
from todo.store import add_todo, load_todos, complete_todo, delete_todo, search_todos
from pathlib import Path


def format_todo(t: dict) -> str:
    status = "x" if t["done"] else " "
    parts = [f"  [{status}] {t['id']}: {t['title']}"]
    priority = t.get("priority")
    due = t.get("due")
    extras = []
    if priority and priority != "medium":
        extras.append(priority)
    if due:
        extras.append(f"due: {due}")
    if extras:
        parts.append(f" ({', '.join(extras)})")
    return "".join(parts)


def print_todos(todos: list[dict]) -> None:
    if not todos:
        print("No todos yet. Add one with: todo add <title>")
        return
    for t in todos:
        print(format_todo(t))


def parse_flag(args: list[str], flag: str) -> str | None:
    if flag in args:
        idx = args.index(flag)
        if idx + 1 < len(args):
            return args[idx + 1]
    return None


def remove_flag(args: list[str], flag: str) -> list[str]:
    if flag not in args:
        return args
    idx = args.index(flag)
    result = args[:idx]
    if idx + 1 < len(args):
        result += args[idx + 2:]
    return result


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: todo <command> [args]")
        print("Commands: list, add, done, delete, search")
        print("Options: --version")
        return

    if "--version" in args:
        print(f"todo-cli {__version__}")
        return

    cmd = args[0]

    if cmd == "list":
        priority_filter = parse_flag(args, "--priority")
        todos = load_todos()
        if priority_filter:
            todos = [t for t in todos if t.get("priority") == priority_filter]
        todos.sort(key=lambda t: (t.get("due") is None, t.get("due") or ""))
        print_todos(todos)

    elif cmd == "add":
        priority = parse_flag(args, "--priority")
        due = parse_flag(args, "--due")
        remaining = remove_flag(remove_flag(args, "--priority"), "--due")
        if len(remaining) < 2:
            print("Usage: todo add <title> [--priority high|medium|low] [--due YYYY-MM-DD]")
            return
        title = " ".join(remaining[1:])
        try:
            todo = add_todo(title, priority=priority or "medium", due=due)
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"Added: [{todo['id']}] {todo['title']}")

    elif cmd == "done":
        if len(args) < 2:
            print("Usage: todo done <id>")
            return
        try:
            todo_id = int(args[1])
        except ValueError:
            print(f"Error: '{args[1]}' is not a valid todo ID. Please provide a number.")
            return
        result = complete_todo(todo_id)
        if result:
            print(f"Completed: {result['title']}")
        else:
            print(f"Todo {todo_id} not found")

    elif cmd == "delete":
        if len(args) < 2:
            print("Usage: todo delete <id>")
            return
        try:
            todo_id = int(args[1])
        except ValueError:
            print(f"Error: '{args[1]}' is not a valid todo ID. Please provide a number.")
            return
        if delete_todo(todo_id):
            print(f"Deleted todo {todo_id}")
        else:
            print(f"Todo {todo_id} not found")

    elif cmd == "search":
        if len(args) < 2:
            print("Usage: todo search <query> [--done | --pending]")
            return
        status_filter = None
        if "--done" in args:
            status_filter = "done"
        elif "--pending" in args:
            status_filter = "pending"
        query_args = [a for a in args[1:] if a not in ("--done", "--pending")]
        query = " ".join(query_args)
        results = search_todos(query, status_filter=status_filter)
        results.sort(key=lambda t: (t.get("due") is None, t.get("due") or ""))
        print_todos(results)

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
