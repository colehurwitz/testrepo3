# todo-cli

![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

A lightweight command-line todo manager written in Python. Add, complete, and delete tasks from your terminal — no dependencies required.

## Features

- **Four commands** — `add`, `list`, `done`, `delete`
- **Persistent storage** — todos saved as JSON in `~/.todo.json`
- **Zero external dependencies** — pure Python standard library
- **Python 3.11+** compatible

## Installation

### From source

```console
$ git clone https://github.com/colehurwitz/testrepo3.git
$ cd testrepo3
$ pip install .
```

This creates the `todo` command via the entry point defined in `pyproject.toml`.

### Development install

```console
$ pip install -e .
```

## Usage

```console
$ todo add "Buy groceries"
Added: [1] Buy groceries

$ todo add "Write README"
Added: [2] Write README

$ todo list
  [ ] 1: Buy groceries
  [ ] 2: Write README

$ todo done 2
Completed: Write README

$ todo list
  [ ] 1: Buy groceries
  [x] 2: Write README

$ todo delete 1
Deleted todo 1

$ todo --version
todo-cli 0.1.0
```

## Data Storage

Todos are persisted as JSON in `~/.todo.json`. The file is created automatically on your first `todo add` call. Each todo entry has three fields:

| Field   | Type   | Description                        |
|---------|--------|------------------------------------|
| `id`    | int    | Auto-incrementing identifier       |
| `title` | string | The task description               |
| `done`  | bool   | Completion status (`false`/`true`) |

## Development

### Prerequisites

- Python 3.11 or higher

### Setup

```console
$ git clone https://github.com/colehurwitz/testrepo3.git
$ cd testrepo3
$ pip install -e .
```

### Run tests

```console
$ python -m pytest tests/ -q
```

### Run without installing

```console
$ python -m todo.cli add "Try it out"
```

### Project structure

```
testrepo3/
├── pyproject.toml       # Package metadata and entry point
├── todo/
│   ├── __init__.py      # Version string
│   ├── cli.py           # Argument parsing and command dispatch
│   └── store.py         # JSON file persistence layer
├── tests/
│   ├── test_cli.py      # CLI integration tests
│   └── test_store.py    # Store unit tests
└── eval/
    └── score.py         # Project evaluation scoring
```
