import sys
from todo.cli import main


def test_version_flag(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["todo", "--version"])
    main()
    captured = capsys.readouterr()
    assert "todo-cli" in captured.out
    assert "0.1.0" in captured.out
