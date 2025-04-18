import json
import subprocess
from pathlib import Path
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest
import toml
import yaml
from typer.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def mock_snow_cli(
    monkeypatch,
    mock_config_toml: Path,
    mock_get_connection: None,  # noqa: ARG001
) -> list[list[str]]:
    """Mock Snowflake CLI main function."""

    from sisx.utils.snowcli import run_snow_command as real_run_snow_command

    call_log = []

    def fake_run_snow_command(
        cmd_args: list[str],
        capture_output: bool = True,  # noqa: ARG001
        check: bool = True,  # noqa: ARG001
        debug: bool = False,  # noqa: ARG001
    ) -> str:
        call_log.append(cmd_args)
        if "--info" in cmd_args:
            return json.dumps(
                [
                    {
                        "key": "default_config_file_path",
                        "value": str(mock_config_toml),
                    }
                ]
            )
        if "init" in cmd_args:
            return real_run_snow_command(cmd_args)
        return ""

    monkeypatch.setattr("sisx.utils.snowcli.run_snow_command", fake_run_snow_command)

    return call_log


@pytest.fixture
def mock_get_connection(monkeypatch, mock_config_toml: Path):
    """Mock get_connection_by_name function."""

    def transform_connection_info(name: str) -> dict[str, Any]:
        # The connection list command returns this structure, not just the raw toml
        # info.
        raw_info = toml.loads(mock_config_toml.read_text())["connections"][name]

        transformed_info = {
            "connection_name": name,
            "parameters": raw_info,
            "is_default": False,
        }
        if name == "default":
            transformed_info["is_default"] = True
        return transformed_info

    def fake_get_connection_by_name(name: str) -> dict[str, Any]:
        return transform_connection_info(name)

    def fake_get_default_connection() -> dict[str, Any]:
        return transform_connection_info("default")

    monkeypatch.setattr("sisx.cli.get_connection_by_name", fake_get_connection_by_name)
    monkeypatch.setattr("sisx.cli.get_default_connection", fake_get_default_connection)


@pytest.fixture
def mock_config_file(tmp_path: Path) -> Path:
    """Create a mock snowflake.yml file.

    Args:
        tmp_path: Pytest fixture that provides a temporary directory unique to each test function.

    Returns:
        Path: Path to the created mock config file.
    """
    config = {
        "definition_version": "2",
        "env": {
            "name": "test_app",
            "database": "TEST_DB",
            "schema": "PUBLIC",
            "role": "ACCOUNTADMIN",
            "preview_database": "PREVIEW_DB",
            "preview_schema": "PREVIEW_SCHEMA",
            "preview_role": "PREVIEW_ROLE",
            "stage": "CUSTOM_STAGE",
            "app_type": "warehouse",
            "query_warehouse": "COMPUTE_WH",
            "app_warehouse": "STREAMLIT_WH",
            "compute_pool": "COMPUTE_POOL",
        },
        "entities": {
            "streamlit_app": {
                "type": "streamlit",
                "identifier": {
                    "name": "test_app",
                    "schema": "PUBLIC",
                    "database": "TEST_DB",
                },
                "stage": "CUSTOM_STAGE",
                "query_warehouse": "COMPUTE_WH",
                "main_file": "streamlit_app.py",
                "pages_dir": "pages/",
                "artifacts": ["**/*.py", "*.yml", "requirements.txt"],
            }
        },
    }
    config_path = tmp_path / "snowflake.yml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    return config_path


@pytest.fixture
def mock_config_toml(tmp_path: Path) -> Path:
    """Create a mock config.toml file.

    Args:
        tmp_path: Pytest fixture that provides a temporary directory unique to each test function.

    Returns:
        Path: Path to the created mock config.toml file.
    """
    config = {
        "connections": {
            "default": {
                "connection_name": "default",
                "account": "test_account",
                "user": "test_user",
                "role": "ACCOUNTADMIN",
                "database": "TEST_DB",
                "schema": "PUBLIC",
                "warehouse": "COMPUTE_WH",
            },
            "test_conn": {
                "connection_name": "test_conn",
                "account": "test_account",
                "user": "test_user",
                "role": "ACCOUNTADMIN",
                "database": "TEST_DB",
                "schema": "PUBLIC",
                "warehouse": "COMPUTE_WH",
            },
        },
    }
    config_path = tmp_path / ".snowflake" / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as f:
        toml.dump(config, f)
    return config_path


@pytest.fixture
def mock_snow_info(mock_config_toml: Path) -> Generator[MagicMock, None, None]:
    """Mock snow --info command, but let other subprocess calls run normally."""
    real_subprocess_run = subprocess.run  # Store the original function

    def mock_run_impl(cmd_args, *args, **kwargs):
        # Only mock snow --info command
        if isinstance(cmd_args, list) and "snow" in cmd_args and "--info" in cmd_args:
            mock_result = MagicMock()
            mock_result.stdout = json.dumps(
                [
                    {
                        "key": "default_config_file_path",
                        "value": str(mock_config_toml),
                    }
                ]
            )
            mock_result.returncode = 0
            return mock_result
        # Use the original subprocess.run for all other calls
        return real_subprocess_run(cmd_args, *args, **kwargs)

    with patch("subprocess.run", side_effect=mock_run_impl) as mock_run:
        yield mock_run
