import sys
from todo import __version__
from todo.store import add_todo, load_todos, complete_todo, delete_todo, search_todos, VALID_PRIORITIES


def print_todos(todos: list[dict]) -> None:
    if not todos:
        print("No todos yet. Add one with: todo add <title>")
        return
    for t in todos:
        status = "x" if t["done"] else " "
        priority = t.get("priority", "medium")
        print(f"  [{status}] {t['id']}: {t['title']} ({priority})")


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
        todos = load_todos()
        rest = args[1:]
        if "--priority" in rest:
            idx = rest.index("--priority")
            if idx + 1 < len(rest):
                pval = rest[idx + 1].lower()
                if pval not in VALID_PRIORITIES:
                    print(f"Invalid priority: {pval}. Choose from: high, medium, low")
                    return
                todos = [t for t in todos if t.get("priority", "medium") == pval]
        print_todos(todos)

    elif cmd == "add":
        if len(args) < 2:
            print("Usage: todo add <title> [--priority high|medium|low]")
            return
        rest = args[1:]
        priority = "medium"
        if "--priority" in rest:
            idx = rest.index("--priority")
            if idx + 1 < len(rest):
                priority = rest[idx + 1].lower()
                if priority not in VALID_PRIORITIES:
                    print(f"Invalid priority: {priority}. Choose from: high, medium, low")
                    return
                rest = rest[:idx] + rest[idx + 2:]
            else:
                print("Usage: todo add <title> [--priority high|medium|low]")
                return
        title = " ".join(rest)
        if not title:
            print("Usage: todo add <title> [--priority high|medium|low]")
            return
        todo = add_todo(title, priority=priority)
        print(f"Added: [{todo['id']}] {todo['title']} ({todo['priority']})")

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
