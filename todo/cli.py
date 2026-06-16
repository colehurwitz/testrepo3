import sys
from todo.store import add_todo, load_todos, complete_todo, delete_todo
from pathlib import Path


def print_todos(todos: list[dict]) -> None:
    if not todos:
        print("No todos yet. Add one with: todo add <title>")
        return
    for t in todos:
        status = "x" if t["done"] else " "
        print(f"  [{status}] {t['id']}: {t['title']}")


def main(argv: list[str] | None = None) -> None:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: todo <command> [args]")
        print("Commands: list, add, done, delete")
        return

    if args[0] in ("--version", "-V"):
        from todo import __version__
        print(f"todo-cli {__version__}")
        return

    cmd = args[0]

    if cmd == "list":
        todos = load_todos()
        print_todos(todos)

    elif cmd == "add":
        if len(args) < 2:
            print("Usage: todo add <title>")
            return
        title = " ".join(args[1:])
        todo = add_todo(title)
        print(f"Added: [{todo['id']}] {todo['title']}")

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
