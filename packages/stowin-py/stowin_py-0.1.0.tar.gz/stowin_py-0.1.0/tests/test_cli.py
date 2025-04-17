from click.testing import CliRunner
from stowin_py.cli import cli
from pathlib import Path

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
