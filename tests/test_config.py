import pytest
from screenshot_to_text.config import read_config
from screenshot_to_text.errors import ConfigNotFoundError, ConfigurationError


def test_config_not_found(tmp_path):
    fake_path = tmp_path / "config.toml"

    with pytest.raises(ConfigNotFoundError):
        read_config(fake_path)


def test_run_missing_config(mocker, tmp_path):
    from typer.testing import CliRunner
    from screenshot_to_text.cli import app

    runner = CliRunner()

    mocker.patch("screenshot_to_text.cli.config_file_path", return_value=tmp_path / "missing.toml")

    with pytest.raises(ConfigurationError):
        runner.invoke(app, ["run"], catch_exceptions=False)
