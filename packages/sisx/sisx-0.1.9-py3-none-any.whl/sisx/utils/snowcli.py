import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any, Optional, Sequence

import typer
from click import ClickException
from snowflake.cli._app.__main__ import main


def run_snow_command(
    cmd_args: Sequence[str],
    capture_output: bool = True,
    check: bool = True,
    debug: bool = False,
) -> Any:
    """Run a snow CLI command with proper UV wrapping."""
    if debug:
        cmd_args = "snow" + " ".join(cmd_args)
        print("Running command:", cmd_args)
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        if capture_output:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                main(cmd_args)
        else:
            main(cmd_args)
    except SystemExit as e:
        if e.code != 0 and check:
            raise ValueError(stdout.getvalue() + "\n" + stderr.getvalue()) from e
    return stdout.getvalue() + "\n" + stderr.getvalue()


def deploy_streamlit(
    *,
    name: str,
    database: str,
    schema: str,
    role: str,
    title: Optional[str] = None,
    replace: bool = False,
    open_browser: bool = False,
    connection: Optional[str] = None,
    query_warehouse: Optional[str] = None,
    app_warehouse: Optional[str] = None,
    verbose: bool = False,
    debug: bool = False,
    extra_args: Sequence[str] | None = None,
) -> Any:
    """Deploy a Streamlit application using the snow CLI."""
    cmd = ["streamlit", "deploy"]

    if replace:
        cmd.append("--replace")

    if open_browser:
        cmd.append("--open")

    if connection:
        cmd.extend(["--connection", connection])

    # Add environment variables
    cmd.append(f"--env=name={name}")
    if title:
        cmd.append(f"--env=title={title}")

    # Add database, schema, and role
    cmd.extend(["--database", database])
    cmd.extend(["--schema", schema])
    cmd.extend(["--role", role])

    # Handle warehouse overrides through env variables
    if query_warehouse:
        cmd.append(f"--env=query_warehouse={query_warehouse}")
    if app_warehouse:
        cmd.append(f"--env=app_warehouse={app_warehouse}")

    cmd.append(f"--env=database={database}")
    cmd.append(f"--env=schema={schema}")
    cmd.append(f"--env=role={role}")

    if verbose:
        cmd.append("--verbose")

    if debug:
        cmd.append("--debug")

    if extra_args:
        cmd.extend(extra_args)

    try:
        run_snow_command(cmd, capture_output=not verbose, check=True, debug=debug)
    except Exception as e:
        raise e


def drop_streamlit(
    app_name: str,
    database: str,
    schema: str,
    connection: Optional[str] = None,
    verbose: bool = False,
) -> Any:
    """Drop a Streamlit application using the snow CLI."""
    full_app_name = f"{database}.{schema}.{app_name}"
    cmd = ["object", "drop", "streamlit", full_app_name]

    if connection:
        cmd.extend(["--connection", connection])

    return run_snow_command(cmd, capture_output=not verbose)


def drop_spcs_services(
    app_name: str,
    connection: Optional[str] = None,
    verbose: bool = False,
) -> Any:
    """Drop SPCS services associated with a Streamlit app."""
    cmd = [
        "sql",
        "-q",
        f"CALL SYSTEM\\$DELETE_RUNNING_STREAMLIT_INSTANCES('{app_name}')",
    ]

    if connection:
        cmd.extend(["--connection", connection])

    return run_snow_command(cmd, capture_output=not verbose, check=False)


def list_streamlit_apps(
    filter_text: Optional[str] = None,
    connection: Optional[str] = None,
    verbose: bool = False,
) -> list[dict[str, Any]]:
    """List Streamlit applications in Snowflake."""
    cmd = ["object", "list", "streamlit", "--format=json"]

    if filter_text:
        cmd.extend(["--like", f"%{filter_text}%"])

    if connection:
        cmd.extend(["--connection", connection])

    if verbose:
        cmd.append("--verbose")

    result = run_snow_command(cmd, capture_output=True)
    return json.loads(result.stdout)


def init_app(
    output_path: Path,
    template_dir: Path,
    template_name: str,
    variables: dict[str, str],
    verbose: bool = False,
    debug: bool = False,
    force: bool = False,
) -> Any:
    """Initialize a new Streamlit application using the snow CLI."""
    # Remove the directory if it exists and force is True
    if output_path.exists():
        if force:
            import shutil

            shutil.rmtree(output_path)
        else:
            raise ClickException(
                f"The directory {output_path} already exists. Please specify a different path for the project."
            )

    # Ensure we have all required variables
    required_vars = {
        "name": output_path.name,  # Use directory name as app name if not provided
        "database": variables.get("database", "streamlit"),
        "schema": variables.get("schema", "public"),
        "role": variables.get("role", "accountadmin"),
        "preview_database": variables.get(
            "preview_database", variables.get("database", "streamlit")
        ),
        "preview_schema": variables.get(
            "preview_schema", variables.get("schema", "public")
        ),
        "preview_role": variables.get(
            "preview_role", variables.get("role", "accountadmin")
        ),
        "app_type": variables.get("app_type", "warehouse"),
    }

    # Update variables with required vars
    variables.update(required_vars)

    cmd = [
        "init",
        str(output_path),
        "--template-source",
        str(template_dir),
        "--template",
        template_name,
        "--no-interactive",
    ]

    # Add all variables as -D parameters
    for key, value in variables.items():
        cmd.extend(["-D", f"{key}={value}"])

    if verbose:
        cmd.append("--verbose")
        typer.echo(f"Command: {' '.join(cmd)}")

    if debug:
        cmd.append("--debug")

    return run_snow_command(cmd, capture_output=not verbose)


def get_snow_info() -> list[dict[str, Any]]:
    """Get information about the snow CLI configuration."""
    result = run_snow_command(["--info"])
    return json.loads(result.stdout)
