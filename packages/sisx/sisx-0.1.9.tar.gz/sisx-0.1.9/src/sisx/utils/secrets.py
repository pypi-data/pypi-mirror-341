from pathlib import Path
from typing import Any


def create_secrets_file(
    output_dir: str | Path,
    connection_config: dict[str, Any],
    compute_config: dict[str, Any],
) -> None:
    """Create the secrets.toml file with connection information."""
    output_path = Path(output_dir)
    secrets_dir = output_path / ".streamlit"
    secrets_dir.mkdir(parents=True, exist_ok=True)
    secrets_path = secrets_dir / "secrets.toml"

    secrets_path.write_text(
        "\n".join(
            [
                "[connections.snowflake]",
                *[
                    f'{key} = "{value}"'
                    for key, value in _get_connection_settings(
                        connection_config["parameters"], compute_config
                    ).items()
                ],
                "",  # Add trailing newline
            ]
        )
    )


def _get_connection_settings(
    connection_config: dict[str, Any],
    compute_config: dict[str, Any],
) -> dict[str, str]:
    """Get connection settings for secrets.toml."""
    # Map of snow config keys to secrets.toml keys
    key_mapping = {
        "account": "account",
        "user": "user",
        "password": "password",
        "private_key": "private_key",
        "private_key_path": "private_key_path",
        "private_key_passphrase": "private_key_passphrase",
        "token": "token",
        "authenticator": "authenticator",
        "role": "role",
        "database": "database",
        "schema": "schema",
        "warehouse": "query_warehouse",
    }

    # Create a dictionary of all connection settings
    connection_settings: dict[str, str] = {}

    # First add all settings from the config file
    for snow_key, secrets_key in key_mapping.items():
        if (
            (value := connection_config.get(snow_key))
            and isinstance(value, str)
            and value != "****"
        ):
            connection_settings[secrets_key] = value

    # Then override with user-specified values
    if compute_config["type"] == "warehouse":
        # Use app_warehouse for the warehouse setting since that's what the app will run on
        app_warehouse = compute_config.get("app_warehouse")
        if isinstance(app_warehouse, str):  # Ensure value is a string
            connection_settings["warehouse"] = app_warehouse
    else:
        connection_settings.pop("warehouse", None)
        compute_pool = compute_config.get("compute_pool")
        if isinstance(compute_pool, str):  # Ensure value is a string
            connection_settings["compute_pool"] = compute_pool

    return connection_settings
