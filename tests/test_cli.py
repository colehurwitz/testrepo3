import sys
import pytest
from unittest.mock import patch
from todo.cli import main, get_version


def run_cli(*args):
    with patch.object(sys, "argv", ["todo", *args]):
        main()


class TestVersion:
    def test_version_long_flag(self, capsys):
        run_cli("--version")
        assert capsys.readouterr().out.strip() == f"todo-cli {get_version()}"

    def test_version_short_flag(self, capsys):
        run_cli("-V")
        assert capsys.readouterr().out.strip() == f"todo-cli {get_version()}"

    def test_version_matches_metadata(self):
        v = get_version()
        assert v != ""
        parts = v.split(".")
        assert len(parts) >= 2


class TestUsage:
    def test_no_args_prints_usage(self, capsys):
        run_cli()
        out = capsys.readouterr().out
        assert "Usage:" in out
        assert "--version" in out

    def test_unknown_command(self, capsys):
        run_cli("bogus")
        assert "Unknown command: bogus" in capsys.readouterr().out
