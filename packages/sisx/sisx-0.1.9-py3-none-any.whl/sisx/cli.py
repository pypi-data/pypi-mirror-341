from __future__ import annotations

import shutil
import subprocess
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from typing import Annotated, Any

import typer
import yaml

from .utils.secrets import create_secrets_file
from .utils.snowcli import (
    deploy_streamlit,
    drop_spcs_services,
    drop_streamlit,
    init_app,
    list_streamlit_apps,
)
from .utils.templates import (
    get_template_dir,
    get_template_variables,
)
from .utils.toml_config import (
    get_connection_by_name,
    get_default_connection,
)
from .utils.yaml_config import _read_snowflake_config

app = typer.Typer(help="sisx CLI tool for Streamlit in Snowflake applications")

# Type aliases for better readability
ComputeConfig = dict[str, Any]


def _version_callback(value: bool) -> None:
    """Print the version of sisx and exit."""
    if value:
        from importlib.metadata import version

        try:
            v = version("sisx")
            typer.echo(f"sisx version: {v}")
        except PackageNotFoundError:
            typer.echo("sisx version: unknown")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show the version and exit.",
        callback=_version_callback,
    ),
) -> None:
    """
    sisx CLI tool for Streamlit in Snowflake applications.
    """


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def deploy(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    replace: bool = typer.Option(
        False, "--replace", "-r", help="Replace the Streamlit app if it already exists"
    ),
    open_browser: Annotated[
        bool,
        typer.Option(
            "--no-open", help="Don't open the deployed Streamlit app in a browser"
        ),
    ] = False,
    connection: str | None = typer.Option(
        None, "--connection", "-c", help="Connection to use for deployment"
    ),
    query_warehouse: str | None = typer.Option(
        None, "--query-warehouse", help="Override the query warehouse to use"
    ),
    app_warehouse: str | None = typer.Option(
        None, "--app-warehouse", help="Override the app warehouse to use"
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output"),
) -> None:
    """
    Deploy a Streamlit application using the Snowflake CLI.

    This command wraps the `snow streamlit deploy` command, providing a convenient
    interface for deploying Streamlit applications to Snowflake.

    By default, opens the app in your browser. Use --no-open to disable.
    """
    args = ctx.args
    config = _read_snowflake_config()

    # Get configuration from env section
    env = config.get("env", {})
    name = env.get("name")
    database = env.get("database")
    schema = env.get("schema")
    role = env.get("role")

    if not all([name, database, schema, role]):
        typer.echo("Missing required configuration in snowflake.yml")
        raise typer.Exit(code=1)

    connection_info = _get_connection(connection, verbose, debug)
    connection_name = connection_info["connection_name"]

    try:
        deploy_streamlit(
            name=name,
            database=database,
            schema=schema,
            role=role,
            replace=replace,
            open_browser=not open_browser,
            connection=connection_name,
            query_warehouse=query_warehouse,
            app_warehouse=app_warehouse,
            verbose=verbose,
            debug=debug,
            extra_args=args,
        )
    except Exception as e:
        typer.echo(f"Error deploying app: {e}")
        raise typer.Exit(code=1) from e

    typer.echo(f"App '{name}' successfully deployed!")


@app.command(name="deploy-preview")
def deploy_preview(
    preview_name: str | None = typer.Option(
        None, "--preview-name", help="Name of the preview app"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    replace: bool = typer.Option(
        False, "--replace", "-r", help="Replace the Streamlit app if it already exists"
    ),
    open_browser: Annotated[
        bool,
        typer.Option(
            "--no-open", help="Don't open the deployed Streamlit app in a browser"
        ),
    ] = False,
    connection: str | None = typer.Option(
        None, "--connection", "-c", help="Connection to use for deployment"
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output"),
) -> None:
    """
    Deploy a preview version of a Streamlit application.

    This command adds 'preview_' to the beginning of the app name and also adds
    'PREVIEW: ' to the app title, making it easy to identify preview deployments.

    By default, opens the app in your browser. Use --no-open to disable.
    """
    config = _read_snowflake_config()

    # Get configuration from env section
    env = config.get("env", {})
    original_name = env.get("name")
    original_title = env.get("title", "Streamlit App")
    preview_database = env.get("preview_database", env.get("database"))
    preview_schema = env.get("preview_schema", env.get("schema"))
    preview_role = env.get("preview_role", env.get("role"))

    if not all([original_name, preview_database, preview_schema, preview_role]):
        typer.echo("Missing required configuration in snowflake.yml")
        raise typer.Exit(code=1)

    if preview_name is None:
        preview_name = f"preview_{original_name}"

    preview_title = f"PREVIEW: {original_title}"

    if verbose:
        typer.echo(f"Creating preview deployment with name: {preview_name}")
        typer.echo(f"Preview title will be: {preview_title}")
        typer.echo(f"Using database: {preview_database}")
        typer.echo(f"Using schema: {preview_schema}")
        typer.echo(f"Using role: {preview_role}")

    try:
        deploy_streamlit(
            name=preview_name,
            database=preview_database,
            schema=preview_schema,
            role=preview_role,
            title=preview_title,
            replace=replace,
            open_browser=not open_browser,
            connection=connection,
            verbose=verbose,
            debug=debug,
        )
    except Exception as e:
        typer.echo(f"Error deploying app: {e}")
        raise typer.Exit(code=1) from e

    typer.echo(f"App '{preview_name}' successfully deployed!")


def _drop_app(
    app_name: str,
    database: str,
    schema: str,
    connection: str | None = None,
    verbose: bool = False,
    drop_spcs: bool = False,
) -> bool:
    """Helper function to drop a Streamlit app and optionally its SPCS services."""
    # First drop any SPCS services associated with the app if requested
    if drop_spcs:
        _drop_app_spcs_services(app_name, connection, verbose)

    try:
        drop_streamlit(
            app_name=app_name,
            database=database,
            schema=schema,
            connection=connection,
            verbose=verbose,
        )
        full_app_name = f"{database}.{schema}.{app_name}"
        typer.echo(f"Successfully dropped app '{full_app_name}'")
        return True
    except Exception as e:
        typer.echo(f"Error dropping Streamlit app: {e}")
        return False


def _drop_app_spcs_services(
    app_name: str,
    connection: str | None = None,
    verbose: bool = False,
) -> bool:
    """Helper function to drop SPCS services associated with a Streamlit app."""
    if verbose:
        typer.echo(f"Dropping associated SPCS services for {app_name}")

    try:
        drop_spcs_services(
            app_name=app_name,
            connection=connection,
            verbose=verbose,
        )
        return True
    except Exception as e:
        typer.echo(
            f"Warning: Error dropping SPCS services for {app_name} (this is usually ok): {e}"
        )
        return False


@app.command()
def drop(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    connection: str | None = typer.Option(
        None, "--connection", "-c", help="Connection to use for deployment"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force drop without confirmation"
    ),
    drop_spcs: bool = typer.Option(
        False, "--drop-spcs", help="Also drop any associated SPCS services"
    ),
) -> None:
    """
    Drop a Streamlit application from Snowflake.

    This command will remove the Streamlit app. If --drop-spcs is specified,
    it will also clean up any associated SPCS services.
    """
    # Read the app name from the yaml file
    try:
        config = yaml.safe_load(Path("snowflake.yml").read_text())
    except Exception as e:
        typer.echo(f"Error reading app configuration from snowflake.yml: {e}")
        raise typer.Exit(code=1) from e

    # Get the app name from env section
    app_name = config.get("env", {}).get("name")
    database = config.get("streamlit", {}).get("database")
    schema = config.get("streamlit", {}).get("schema")

    if verbose:
        typer.echo(
            f"Found configuration: app={app_name}, db={database}, schema={schema}"
        )

    # Create the fully qualified name
    full_app_name = f"{database}.{schema}.{app_name}"

    if verbose:
        typer.echo(f"Dropping Streamlit app: {full_app_name}")

    # Confirm unless --force is specified
    if not force:
        confirm = typer.confirm(
            f"Are you sure you want to drop the app '{full_app_name}'?"
        )
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()

    # Use the helper function to drop the app
    success = _drop_app(app_name, database, schema, connection, verbose, drop_spcs)
    if not success:
        raise typer.Exit(code=1)


@app.command(name="drop-preview")
def drop_preview(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    connection: str = typer.Option(
        None, "--connection", "-c", help="Connection to use for deployment"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force drop without confirmation"
    ),
    drop_spcs: bool = typer.Option(
        False, "--drop-spcs", help="Also drop any associated SPCS services"
    ),
):
    """
    Drop a preview version of a Streamlit application from Snowflake.

    This command will remove the preview Streamlit app (with prefix 'preview_').
    If --drop-spcs is specified, it will also clean up any associated SPCS services.
    """
    try:
        config = yaml.safe_load(Path("snowflake.yml").read_text())
    except (yaml.YAMLError, OSError) as e:
        typer.echo(f"Error reading app configuration from snowflake.yml: {e}")
        raise typer.Exit(code=1) from e

    # Get the app name from env section and add preview prefix
    original_name = config.get("env", {}).get("name")
    preview_name = f"preview_{original_name}"
    database = config.get("streamlit", {}).get("database")
    schema = config.get("streamlit", {}).get("schema")

    if verbose:
        typer.echo(
            f"Found configuration: app={preview_name}, db={database}, schema={schema}"
        )

    if not original_name or not database or not schema:
        typer.echo("Error: Missing required configuration in snowflake.yml")
        raise typer.Exit(code=1)

    # Create the fully qualified name
    full_preview_name = f"{database}.{schema}.{preview_name}"

    if verbose:
        typer.echo(f"Dropping preview Streamlit app: {full_preview_name}")

    # Confirm unless --force is specified
    if not force:
        confirm = typer.confirm(
            f"Are you sure you want to drop the preview app '{full_preview_name}'?"
        )
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()

    # Use the helper function to drop the app
    success = _drop_app(preview_name, database, schema, connection, verbose, drop_spcs)
    if not success:
        raise typer.Exit(code=1)


@app.command()
def new(
    output_dir: str | None = typer.Argument(
        None, help="Directory where the new app will be created"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force creation of app, overwriting existing directory",
    ),
    connection: str | None = typer.Option(
        None,
        "--connection",
        "-c",
        help="Name of the connection to use",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    compute_type: str | None = typer.Option(
        "warehouse",
        "--compute-type",
        "-t",
        help="Type of compute to use: 'warehouse' or 'compute_pool'",
    ),
    query_warehouse: str | None = typer.Option(
        None,
        "--query-warehouse",
        "-q",
        help="Warehouse to use for queries (when using warehouse compute type)",
    ),
    app_warehouse: str | None = typer.Option(
        None,
        "--app-warehouse",
        "-a",
        help="Warehouse to use for running the app (when using warehouse compute type)",
    ),
    compute_pool: str | None = typer.Option(
        None,
        "--compute-pool",
        help="Compute pool to use (when using compute_pool compute type)",
    ),
    stage: str | None = typer.Option(
        None, "--stage", help="Stage to use for app artifacts"
    ),
    database: str | None = typer.Option(
        None, "--database", help="Database to use for the app"
    ),
    schema: str | None = typer.Option(
        None, "--schema", help="Schema to use for the app"
    ),
    role: str | None = typer.Option(None, "--role", help="Role to use for the app"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output"),
) -> None:
    """
    Create a new Streamlit in Snowflake application using a template.

    This command uses snow init to generate a new app from the appropriate template
    based on your compute choice (warehouse or compute pool).

    All configuration can be provided via command line flags for automation, or
    will be prompted for interactively if not provided.
    """
    if verbose:
        typer.echo(f"Creating new Streamlit app in {output_dir}")

    if output_dir is None:
        output_dir = _get_output_dir()

    # Get connection info - either from flag or interactive
    current_connection = _get_connection(connection, verbose, debug)

    # Get compute configuration - either from flags or interactive, defaulting to
    # values from the current connection
    compute_config = {}
    if compute_type is not None and compute_type not in ["warehouse", "compute_pool"]:
        typer.echo("compute-type must be either 'warehouse' or 'compute_pool'")
        raise typer.Exit(code=1)
    if compute_type is None:
        compute_type = "warehouse"
    compute_config["type"] = compute_type

    if query_warehouse is not None:
        compute_config["query_warehouse"] = query_warehouse
    if app_warehouse is not None:
        compute_config["app_warehouse"] = app_warehouse
    if compute_pool is not None:
        compute_config["compute_pool"] = compute_pool
    if stage is not None:
        compute_config["stage"] = stage
    if database is not None:
        compute_config["database"] = database
    if schema is not None:
        compute_config["schema"] = schema
    if role is not None:
        compute_config["role"] = role

    compute_config = _get_compute_configuration(compute_config, current_connection)

    template_name = "app"  # Use the unified template
    compute_config["app_type"] = compute_type  # Add app_type to compute_config

    template_dir = get_template_dir()
    output_path = Path(output_dir)

    if output_path.exists():
        if force:
            shutil.rmtree(output_path)
        else:
            typer.echo(f"Error: Output directory {output_path} already exists")
            raise typer.Exit(code=1)

    template_variables = get_template_variables(output_path, compute_config)

    try:
        init_app(
            output_path=output_path,
            template_dir=template_dir,
            template_name=template_name,
            variables=template_variables,
            verbose=verbose,
            debug=debug,
            force=force,
        )
    except Exception as e:
        typer.echo(f"Error creating new Streamlit app: {e}")
        raise typer.Exit(code=1) from e

    # Delete the unused dependency file based on compute type
    try:
        if compute_type == "compute_pool":
            # For compute pool, delete environment.yml
            env_file = output_path / "environment.yml"
            if env_file.exists():
                env_file.unlink()
                if verbose:
                    typer.echo(
                        "Removed environment.yml as compute_pool app uses requirements.txt"
                    )
        else:
            # For warehouse, delete requirements.txt
            req_file = output_path / "requirements.txt"
            if req_file.exists():
                req_file.unlink()
                if verbose:
                    typer.echo(
                        "Removed requirements.txt as warehouse app uses environment.yml"
                    )
    except OSError as e:
        typer.echo(f"Warning: Error cleaning up unused dependency file: {e}")

    # Create secrets.toml after snow init succeeds
    try:
        create_secrets_file(output_path, current_connection, compute_config)
    except OSError as e:
        typer.echo(f"Error creating secrets.toml: {e}")
        raise typer.Exit(code=1) from e

    typer.echo(f"Successfully created new Streamlit app in {output_dir}!")


def _get_connection(
    name: str | None = None, verbose: bool = False, debug: bool = False
) -> dict[str, Any]:
    """Look up either the named connection or the default connection, and if not found
    then create a new connection."""
    if name is not None:
        try:
            current_connection = get_connection_by_name(name)
        except ValueError:
            # Run the new connection command
            typer.echo(f"Connection '{name}' not found. Creating new connection...")
            cmd = ["new-connection", "--connection-name", name]
            if verbose:
                cmd.append("--verbose")
            if debug:
                cmd.append("--debug")
            app(cmd, standalone_mode=False)
            current_connection = get_connection_by_name(name)
    else:
        try:
            current_connection = get_default_connection()
        except ValueError:
            typer.echo("No default connection found. Creating new connection...")
            cmd = ["new-connection"]
            if verbose:
                cmd.append("--verbose")
            if debug:
                cmd.append("--debug")
            app(cmd, standalone_mode=False)
            current_connection = get_default_connection()

    return current_connection


def _get_output_dir() -> str:
    """Get the output directory from the user."""
    return typer.prompt("Enter the directory where the new app will be created")


def _get_compute_configuration(
    compute_config: dict[str, Any],
    current_connection: dict[str, Any],
) -> dict[str, Any]:
    """Get compute configuration interactively from the user."""

    # Use values from compute_config if they exist, otherwise prompt
    compute_config["database"] = compute_config.get("database") or typer.prompt(
        "What database should be used?",
        default=current_connection.get("database", "streamlit"),
    )
    compute_config["schema"] = compute_config.get("schema") or typer.prompt(
        "What schema should be used?",
        default=current_connection.get("schema", "public"),
    )
    compute_config["role"] = compute_config.get("role") or typer.prompt(
        "What role should be used?",
        default=current_connection.get("role", "ACCOUNTADMIN"),
    )

    # Set preview values to the same as main values if not provided
    if not all(
        key in compute_config
        for key in ["preview_database", "preview_schema", "preview_role"]
    ):
        compute_config["preview_database"] = compute_config["database"]
        compute_config["preview_schema"] = compute_config["schema"]
        compute_config["preview_role"] = compute_config["role"]

    if "type" not in compute_config:
        compute_type = typer.prompt(
            "Choose your compute type:\n1. Warehouse (traditional Snowflake warehouse)\n2. Compute Pool (serverless compute)",
            type=str,
            default="1",
        )
        if compute_type not in ["1", "2"]:
            typer.echo("Invalid compute type selected")
            raise typer.Exit(code=1)
        compute_config["type"] = "warehouse" if compute_type == "1" else "compute_pool"

    if compute_config["type"] == "warehouse":
        if "query_warehouse" not in compute_config:
            compute_config["query_warehouse"] = typer.prompt(
                "What warehouse should be used for queries?",
                default=current_connection.get("warehouse", "compute_wh"),
            )
        if "app_warehouse" not in compute_config:
            compute_config["app_warehouse"] = typer.prompt(
                "What warehouse should be used to run the app?",
                default="SYSTEM$STREAMLIT_NOTEBOOK_WH",
            )
    else:
        if "compute_pool" not in compute_config:
            compute_config["compute_pool"] = typer.prompt(
                "What compute pool should be used?", default="streamlit_compute_pool"
            )

    # Set stage to None if not provided
    if "stage" not in compute_config:
        compute_config["stage"] = None

    return compute_config


@app.command()
def run(
    app_path: str = typer.Argument(
        "streamlit_app.py", help="Path to the Streamlit app file to run"
    ),
) -> None:
    """
    Run a Streamlit application locally.

    This command wraps the `streamlit run` command, providing a convenient
    interface for running Streamlit applications during development.
    """
    # Run uv sync first to make sure all dependencies are installed
    typer.echo("Installing/updating dependencies...")

    subprocess.run(["uv", "sync"], check=True)

    typer.echo(f"Running Streamlit app: {app_path}")

    # Base command, use uv so that it automatically runs with the right dependencies
    cmd = ["uv", "run", "streamlit", "run", app_path]

    try:
        # Execute the command
        subprocess.run(cmd, check=True)
    except Exception as e:
        typer.echo(f"Error running Streamlit app: {e}")
        raise typer.Exit(code=1) from e


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def test(ctx: typer.Context) -> None:
    """
    Run the tests for the CLI.
    """
    # Arbitrary arguments are passed to pytest
    args = ctx.args

    subprocess.run(["pytest", *args])


@app.command()
def cleanup(
    filter_text: str | None = typer.Argument(
        None, help="Text to filter apps by (uses preview_ if not specified)"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    connection: str | None = typer.Option(
        None, "--connection", "-c", help="Connection to use for deployment"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force cleanup without confirmation"
    ),
    drop_spcs: bool = typer.Option(
        False, "--drop-spcs", help="Also drop any associated SPCS services"
    ),
) -> None:
    """
    Drop multiple Streamlit applications containing the specified filter text.

    If no filter is provided, uses the text 'preview_' as the filter.
    This is useful for cleaning up development apps in your account.
    """
    if filter_text is None:
        filter_text = "preview_"
        if verbose:
            typer.echo("No filter provided. Using 'preview_' as filter")

    try:
        apps = list_streamlit_apps(
            filter_text=filter_text,
            connection=connection,
            verbose=verbose,
        )
    except Exception as e:
        typer.echo(f"Error listing apps: {e}")
        raise typer.Exit(code=1) from e

    if not apps:
        typer.echo(f"No apps found matching filter: {filter_text}")
        return

    # Display the apps to be deleted
    typer.echo(f"Found {len(apps)} app(s) matching filter '{filter_text}':")
    for app in apps:
        full_name = f"{app['database_name']}.{app['schema_name']}.{app['name']}"
        typer.echo(f" - {full_name}")

    # Confirm deletion unless --force is specified
    if not force:
        confirm = typer.confirm("Are you sure you want to drop all these apps?")
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()

    # Drop each app
    dropped_count = 0
    for app in apps:
        database = app["database_name"]
        schema = app["schema_name"]
        app_name = app["name"]
        full_name = f"{database}.{schema}.{app_name}"

        typer.echo(f"Dropping app: {full_name}")

        # Use the helper function to drop the app
        success = _drop_app(app_name, database, schema, connection, verbose, drop_spcs)
        if success:
            dropped_count += 1

    typer.echo(
        f"Successfully cleaned up {dropped_count} of {len(apps)} app(s) matching filter '{filter_text}'"
    )


@app.command()
def new_connection(
    connection_name: str = typer.Option(
        None,
        "--connection-name",
        "-n",
        help="Name of the new connection.",
    ),
    account: str = typer.Option(
        None,
        "--account",
        "--accountname",
        "-a",
        help="Account name to use when authenticating with Snowflake.",
    ),
    user: str = typer.Option(
        None,
        "--user",
        "--username",
        "-u",
        help="Username to connect to Snowflake.",
    ),
    password: str = typer.Option(
        None,
        "--password",
        "-p",
        help="Snowflake password.",
    ),
    role: str = typer.Option(
        None,
        "--role",
        "--rolename",
        "-r",
        help="Role to use on Snowflake.",
    ),
    warehouse: str = typer.Option(
        None,
        "--warehouse",
        "-w",
        help="Warehouse to use on Snowflake.",
    ),
    database: str = typer.Option(
        None,
        "--database",
        "--dbname",
        "-d",
        help="Database to use on Snowflake.",
    ),
    schema: str = typer.Option(
        None,
        "--schema",
        "--schemaname",
        "-s",
        help="Schema to use on Snowflake.",
    ),
    host: str = typer.Option(
        None,
        "--host",
        "-h",
        help="Host name the connection attempts to connect to Snowflake.",
    ),
    port: int = typer.Option(
        None,
        "--port",
        "-P",
        help="Port to communicate with on the host.",
    ),
    region: str = typer.Option(
        None,
        "--region",
        "-R",
        help="Region name if not the default Snowflake deployment.",
    ),
    authenticator: str = typer.Option(
        None,
        "--authenticator",
        "-A",
        help="Chosen authenticator, if other than password-based",
    ),
    private_key: str = typer.Option(
        None,
        "--private-key",
        "--private-key-file",
        "--private-key-path",
        "-k",
        help="Path to file containing private key",
    ),
    token_file_path: str = typer.Option(
        None,
        "--token-file-path",
        "-t",
        help="Path to file with an OAuth token that should be used when connecting to Snowflake",
    ),
    default: bool = typer.Option(
        False,
        "--default",
        help="If provided the connection will be configured as default connection.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug output",
    ),
) -> None:
    """
    Add a new Snowflake connection configuration.

    This command wraps the `snow connection add` command, providing a convenient
    interface for adding new Snowflake connections.
    """
    cmd = ["connection", "add"]

    # Prompt for required values if not provided
    if connection_name is None:
        connection_name = typer.prompt("Enter connection name", default="default")
    if account is None:
        account = typer.prompt("Enter Snowflake account name")
    if user is None:
        user = typer.prompt("Enter Snowflake username")
    if password is None:
        password = typer.prompt("Enter Snowflake password", hide_input=True)
    if role is None:
        role = typer.prompt("Enter role name", default="ACCOUNTADMIN")
    if warehouse is None:
        warehouse = typer.prompt("Enter warehouse name", default="COMPUTE_WH")
    if database is None:
        database = typer.prompt("Enter database name", default="STREAMLIT")
    if schema is None:
        schema = typer.prompt("Enter schema name", default="PUBLIC")

    # Optional values that we'll only prompt for if user wants to provide them
    if (
        typer.confirm("Do you want to specify a custom host?", default=False)
        and host is None
    ):
        host = typer.prompt("Enter host name")

    if (
        typer.confirm("Do you want to specify a custom port?", default=False)
        and port is None
    ):
        port = typer.prompt("Enter port number", type=int)

    if (
        typer.confirm("Do you want to specify a custom region?", default=False)
        and region is None
    ):
        region = typer.prompt("Enter region name")

    if (
        typer.confirm("Do you want to use a different authenticator?", default=False)
        and authenticator is None
    ):
        authenticator = typer.prompt("Enter authenticator")

    if (
        typer.confirm("Do you want to use private key authentication?", default=False)
        and private_key is None
    ):
        private_key = typer.prompt("Enter path to private key file")

    if (
        typer.confirm("Do you want to use OAuth token authentication?", default=False)
        and token_file_path is None
    ):
        token_file_path = typer.prompt("Enter path to OAuth token file")

    if default is None:
        default = typer.confirm("Set this as the default connection?", default=False)

    # Add all non-None options to the command
    if connection_name:
        cmd.extend(["--connection-name", connection_name])
    if account:
        cmd.extend(["--account", account])
    if user:
        cmd.extend(["--user", user])
    if password:
        cmd.extend(["--password", password])
    if role:
        cmd.extend(["--role", role])
    if warehouse:
        cmd.extend(["--warehouse", warehouse])
    if database:
        cmd.extend(["--database", database])
    if schema:
        cmd.extend(["--schema", schema])
    if host:
        cmd.extend(["--host", host])
    if port:
        cmd.extend(["--port", str(port)])
    if region:
        cmd.extend(["--region", region])
    if authenticator:
        cmd.extend(["--authenticator", authenticator])
    if private_key:
        cmd.extend(["--private-key", private_key])
    if token_file_path:
        cmd.extend(["--token-file-path", token_file_path])
    if default:
        cmd.append("--default")
    if verbose:
        cmd.append("--verbose")
    if debug:
        cmd.append("--debug")

    # Disable interactive mode in the snowcli, since we've already gathered
    # all required values
    cmd.append("--no-interactive")

    try:
        from .utils.snowcli import run_snow_command

        run_snow_command(cmd, capture_output=not verbose)
        typer.echo("Successfully added new Snowflake connection!")
    except Exception as e:
        typer.echo(f"Error adding Snowflake connection: {e}")
        raise typer.Exit(code=1) from e


def main() -> None:
    """
    Main entry point for the CLI.
    """
    return app(prog_name="sisx")


if __name__ == "__main__":
    main()
