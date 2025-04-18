from typer.testing import CliRunner

from sisx.cli import app


def test_version(runner: CliRunner):
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "sisx version:" in result.stdout
