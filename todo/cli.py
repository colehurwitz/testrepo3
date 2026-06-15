import argparse
import sys
from todo.store import add_todo, load_todos, complete_todo, delete_todo


PRIORITY_LABELS = {"high": "H", "medium": "M", "low": "L"}


def print_todos(todos: list[dict]) -> None:
    if not todos:
        print("No todos yet. Add one with: todo add <title>")
        return
    for t in todos:
        status = "x" if t["done"] else " "
        label = PRIORITY_LABELS[t["priority"]]
        print(f"  [{status}] {t['id']}: [{label}] {t['title']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A simple CLI todo app")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Add a new todo")
    add_p.add_argument("title", nargs="+", help="Todo title")
    add_p.add_argument(
        "-p", "--priority",
        choices=["high", "medium", "low"],
        default="medium",
        help="Priority level (default: medium)",
    )

    list_p = sub.add_parser("list", help="List todos")
    list_p.add_argument(
        "-p", "--priority",
        choices=["high", "medium", "low"],
        default=None,
        help="Filter by priority",
    )

    done_p = sub.add_parser("done", help="Mark a todo as done")
    done_p.add_argument("id", type=int, help="Todo ID")

    del_p = sub.add_parser("delete", help="Delete a todo")
    del_p.add_argument("id", type=int, help="Todo ID")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.command:
        parser.print_help()
        return

    if args.command == "list":
        todos = load_todos()
        if args.priority:
            todos = [t for t in todos if t["priority"] == args.priority]
        print_todos(todos)

    elif args.command == "add":
        title = " ".join(args.title)
        todo = add_todo(title, priority=args.priority)
        print(f"Added: [{todo['id']}] {todo['title']}")

    elif args.command == "done":
        result = complete_todo(args.id)
        if result:
            print(f"Completed: {result['title']}")
        else:
            print(f"Todo {args.id} not found")

    elif args.command == "delete":
        if delete_todo(args.id):
            print(f"Deleted todo {args.id}")
        else:
            print(f"Todo {args.id} not found")


if __name__ == "__main__":
    main()
