from importlib.metadata import version

from todo.cli import main


def test_version_long_flag(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["todo", "--version"])
    main()
    assert capsys.readouterr().out.strip() == version("todo-cli")


def test_version_short_flag(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["todo", "-V"])
    main()
    assert capsys.readouterr().out.strip() == version("todo-cli")
