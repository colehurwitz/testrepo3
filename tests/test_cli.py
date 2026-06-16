import subprocess
import sys


def test_version_long_flag():
    result = subprocess.run(
        [sys.executable, "-m", "todo.cli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "todo-cli" in result.stdout
    assert "0.1.0" in result.stdout


def test_version_short_flag():
    result = subprocess.run(
        [sys.executable, "-m", "todo.cli", "-v"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "todo-cli" in result.stdout
    assert "0.1.0" in result.stdout
