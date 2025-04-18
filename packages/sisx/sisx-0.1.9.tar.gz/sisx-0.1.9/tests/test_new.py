# ruff: noqa: ARG001

import os
from pathlib import Path

import yaml
from typer.testing import CliRunner

from sisx.cli import app


def test_new_command_warehouse_basic(
    runner: CliRunner,
    mock_snow_cli: list[list[str]],
    mock_get_connection: None,
    tmp_path: Path,
):
    app_path = tmp_path / "streamlit_app"

    """Test basic warehouse app creation."""
    result = runner.invoke(
        app,
        [
            "new",
            str(app_path),
            "--compute-type",
            "warehouse",
            "--query-warehouse",
            "COMPUTE_WH",
            "--app-warehouse",
            "STREAMLIT_WH",
            "--force",
        ],
    )

    call_args = mock_snow_cli[-1]

    assert result.exit_code == 0
    assert "Successfully created new Streamlit app" in result.stdout

    # Verify snow init was called with correct args
    assert "init" in call_args
    assert "--template" in call_args
    assert "app" in call_args
    assert "compute_pool=" in call_args

    # Check config files were created
    assert (app_path / "snowflake.yml").exists()
    assert (app_path / ".streamlit" / "secrets.toml").exists()

    # Check correct dependency file exists and other was deleted
    assert (app_path / "environment.yml").exists()
    assert not (app_path / "requirements.txt").exists()

    # Verify environment.yml content
    env_content = yaml.safe_load((app_path / "environment.yml").read_text())
    assert env_content["name"] == "streamlit_app"
    assert "snowflake" in env_content["channels"]
    assert any(dep.startswith("python=3.11.9") for dep in env_content["dependencies"])
    assert any(
        dep.startswith("streamlit=1.39.0") for dep in env_content["dependencies"]
    )
    assert any(
        dep.startswith("snowflake-snowpark-python=1.23.0")
        for dep in env_content["dependencies"]
    )


def test_new_command_compute_pool_basic(
    runner: CliRunner,
    mock_snow_cli: list[list[str]],
    mock_config_file: Path,
    tmp_path: Path,
):
    """Test basic compute pool app creation."""
    result = runner.invoke(
        app,
        [
            "new",
            str(tmp_path),
            "--compute-type",
            "compute_pool",
            "--compute-pool",
            "TEST_POOL",
            "--force",
            "--connection",
            "default",
            "--debug",
            "--database",
            "streamlit",
            "--schema",
            "public",
            "--role",
            "ACCOUNTADMIN",
        ],
    )

    print(result.stdout)
    assert result.exit_code == 0
    assert "Successfully created new Streamlit app" in result.stdout

    # Verify snow init was called with correct args
    call_args = mock_snow_cli[-1]
    assert "app" in call_args
    assert "compute_pool=TEST_POOL" in call_args
    assert "query_warehouse=" in call_args

    # Check config files were created
    assert (tmp_path / "snowflake.yml").exists()
    assert (tmp_path / ".streamlit" / "secrets.toml").exists()

    # Check correct dependency file exists and other was deleted
    assert (tmp_path / "requirements.txt").exists()
    assert not (tmp_path / "environment.yml").exists()

    # Verify requirements.txt content
    req_content = (tmp_path / "requirements.txt").read_text().splitlines()
    assert "streamlit>=1.24.0" in req_content
    assert "snowflake-snowpark-python==1.23.0" in req_content
    assert "streamlit-extras" in req_content
    assert "pandas" in req_content
    assert "numpy" in req_content
    assert "plotly" in req_content


def test_new_command_with_preview_settings(
    runner: CliRunner,
    mock_snow_cli: list[list[str]],
    tmp_path: Path,
):
    """Test app creation with preview deployment settings."""
    result = runner.invoke(
        app,
        [
            "new",
            str(tmp_path),
            "--compute-type",
            "warehouse",
            "--query-warehouse",
            "COMPUTE_WH",
            "--app-warehouse",
            "STREAMLIT_WH",
            "--force",
        ],
    )

    assert result.exit_code == 0

    # Verify snow init was called with correct args
    mock_snow_cli[-1]

    snowflake_yml = tmp_path / "snowflake.yml"
    config = yaml.safe_load(snowflake_yml.read_text())

    # Check preview settings
    assert config["env"]["preview_database"] == config["env"]["database"]
    assert config["env"]["preview_schema"] == config["env"]["schema"]
    assert config["env"]["preview_role"] == config["env"]["role"]


def test_new_command_with_stage(
    runner: CliRunner,
    mock_snow_cli: list[list[str]],
    tmp_path: Path,
):
    """Test app creation with custom stage."""
    result = runner.invoke(
        app,
        [
            "new",
            str(tmp_path),
            "--compute-type",
            "warehouse",
            "--query-warehouse",
            "COMPUTE_WH",
            "--app-warehouse",
            "STREAMLIT_WH",
            "--stage",
            "CUSTOM_STAGE",
            "--force",
            "--connection",
            "default",
            "--debug",
            "--database",
            "streamlit",
            "--schema",
            "public",
            "--role",
            "ACCOUNTADMIN",
        ],
    )

    assert result.exit_code == 0
    assert "Successfully created new Streamlit app" in result.stdout

    # Verify snow init was called with correct args
    mock_snow_cli[-1]

    # Verify stage was set in the generated snowflake.yml
    snowflake_yml = tmp_path / "snowflake.yml"
    assert snowflake_yml.exists()
    config = yaml.safe_load(snowflake_yml.read_text())
    assert config["env"]["stage"] == "CUSTOM_STAGE"


def test_new_command_existing_directory(
    runner: CliRunner,
    mock_snow_cli: list[list[str]],
    tmp_path: Path,
):
    """Test app creation when directory exists without force flag."""
    # Create the directory first
    os.makedirs(tmp_path, exist_ok=True)

    result = runner.invoke(
        app,
        [
            "new",
            str(tmp_path),
            "--compute-type",
            "warehouse",
            "--query-warehouse",
            "COMPUTE_WH",
            "--app-warehouse",
            "STREAMLIT_WH",
        ],
    )

    assert result.exit_code == 1
    assert "already exists" in result.stdout


def test_new_command_invalid_compute_type(
    runner: CliRunner,
    mock_snow_cli: list[list[str]],
    tmp_path: Path,
):
    """Test app creation with invalid compute type."""
    result = runner.invoke(
        app,
        ["new", str(tmp_path), "--compute-type", "invalid", "--force"],
    )

    assert result.exit_code == 1
    assert "compute-type must be either 'warehouse' or 'compute_pool'" in result.stdout
