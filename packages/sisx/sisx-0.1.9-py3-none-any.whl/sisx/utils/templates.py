import json
from importlib import resources
from pathlib import Path
from typing import Any


def get_template_dir() -> Path:
    with resources.path("sisx", "templates") as templates_path:
        return templates_path


def get_template_variables(
    output_dir: Path, compute_config: dict[str, Any]
) -> dict[str, Any]:
    variables = {
        "name": output_dir.name,
        "schema": compute_config["schema"],
        "database": compute_config["database"],
        "role": compute_config["role"],
        "preview_database": compute_config.get(
            "preview_database", compute_config["database"]
        ),
        "preview_schema": compute_config.get(
            "preview_schema", compute_config["schema"]
        ),
        "preview_role": compute_config.get("preview_role", compute_config["role"]),
        "app_type": compute_config["app_type"],
    }

    # Add env section variables
    env_variables = {
        "name": variables["name"],
        "schema": variables["schema"],
        "database": variables["database"],
        "role": variables["role"],
        "preview_database": variables["preview_database"],
        "preview_schema": variables["preview_schema"],
        "preview_role": variables["preview_role"],
        "app_type": variables["app_type"],
    }

    if compute_config["type"] == "warehouse":
        variables["query_warehouse"] = compute_config["query_warehouse"]
        variables["app_warehouse"] = compute_config["app_warehouse"]
        variables["artifacts"] = (
            '"**/*.py", "*.yml"'  # No requirements.txt for warehouse apps
        )
        env_variables["query_warehouse"] = compute_config["query_warehouse"]
        env_variables["app_warehouse"] = compute_config["app_warehouse"]
        variables["compute_pool"] = ""
        env_variables["compute_pool"] = ""
    else:
        variables["compute_pool"] = compute_config["compute_pool"]
        variables["artifacts"] = (
            '"**/*.py", "requirements.txt", "*.yml"'  # Include requirements.txt for compute pool apps
        )
        env_variables["compute_pool"] = compute_config["compute_pool"]
        variables["query_warehouse"] = ""
        env_variables["query_warehouse"] = ""
        variables["app_warehouse"] = ""
        env_variables["app_warehouse"] = ""

    if "stage" in compute_config:
        variables["stage"] = compute_config["stage"]
        env_variables["stage"] = compute_config["stage"]

    variables["env"] = json.dumps(env_variables)

    return variables
