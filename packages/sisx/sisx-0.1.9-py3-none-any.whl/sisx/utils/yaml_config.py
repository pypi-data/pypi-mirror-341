from pathlib import Path
from typing import Any

import typer
import yaml

app = typer.Typer(help="sisx CLI tool for Streamlit in Snowflake applications")

# Type aliases for better readability
SnowflakeConfig = dict[str, Any]
ComputeConfig = dict[str, Any]


def _read_snowflake_config() -> SnowflakeConfig:
    """Read the snowflake.yml file and return the config."""
    try:
        return yaml.safe_load(Path("snowflake.yml").read_text())
    except (yaml.YAMLError, OSError) as e:
        typer.echo(f"Error reading app configuration from snowflake.yml: {e}")
        raise typer.Exit(code=1) from e
