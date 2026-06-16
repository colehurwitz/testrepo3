import subprocess
import sys


def test_version_long_flag():
    result = subprocess.run(
        [sys.executable, "-m", "todo.cli", "--version"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert result.stdout.startswith("todo-cli ")


def test_version_short_flag():
    result = subprocess.run(
        [sys.executable, "-m", "todo.cli", "-V"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert result.stdout.startswith("todo-cli ")


def test_version_flags_match():
    long = subprocess.run(
        [sys.executable, "-m", "todo.cli", "--version"],
        capture_output=True, text=True,
    )
    short = subprocess.run(
        [sys.executable, "-m", "todo.cli", "-V"],
        capture_output=True, text=True,
    )
    assert long.stdout == short.stdout


def test_version_matches_metadata():
    from importlib.metadata import version
    expected = version("todo-cli")
    result = subprocess.run(
        [sys.executable, "-m", "todo.cli", "--version"],
        capture_output=True, text=True,
    )
    assert result.stdout.strip() == f"todo-cli {expected}"
