import pytest
from todo.cli import main
from todo import __version__


@pytest.mark.parametrize("flag", ["--version", "-V"])
def test_version_flag(flag, capsys):
    main([flag])
    output = capsys.readouterr().out.strip()
    assert output == f"todo-cli {__version__}"


def test_version_flag_ignores_trailing_args(capsys):
    main(["--version", "add", "buy milk"])
    output = capsys.readouterr().out.strip()
    assert output == f"todo-cli {__version__}"


def test_unknown_command(capsys):
    main(["bogus"])
    output = capsys.readouterr().out.strip()
    assert output == "Unknown command: bogus"
