import json
from typing import Any

from sisx.utils.snowcli import run_snow_command


def get_all_connections() -> list[dict[str, Any]]:
    result = run_snow_command(["connection", "list", "--format=json"])
    connections = json.loads(result)

    if len(connections) == 0:
        raise ValueError("No connections found. Create one with `sisx new-connection`")

    return connections


def get_connection_by_name(name: str) -> dict[str, Any]:
    info = get_all_connections()

    for item in info:
        if item["connection_name"] == name:
            return item

    raise ValueError(f"No connection found for {name}")


def get_default_connection() -> dict[str, Any]:
    info = get_all_connections()

    for item in info:
        if item["is_default"]:
            return item

    raise ValueError(
        "No default connection found. Create one with `sisx connection add`"
    )
