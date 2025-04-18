# sisx

A command-line interface (CLI) for managing Streamlit applications in Snowflake.

## Overview

`sisx` provides a set of commands to simplify the workflow for developing, deploying, and managing Streamlit applications on Snowflake. It handles common tasks like deploying applications, creating preview versions, and cleaning up old deployments.

## Installation

```bash
uv tool install sisx

# Or

pip install sisx
```

If you don't want to actually install the tool permanently, you can just run `uvx sisx <any command>` to use it.

<!-- [[[cog
import cog
import subprocess

output = subprocess.run(["typer", "sisx.cli", "utils", "docs"], capture_output=True, text=True)
cog.outl(output.stdout)
]]] -->
# CLI

sisx CLI tool for Streamlit in Snowflake applications

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Show the version and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `deploy`: Deploy a Streamlit application using the...
* `deploy-preview`: Deploy a preview version of a Streamlit...
* `drop`: Drop a Streamlit application from Snowflake.
* `drop-preview`: Drop a preview version of a Streamlit...
* `new`: Create a new Streamlit in Snowflake...
* `run`: Run a Streamlit application locally.
* `test`: Run the tests for the CLI.
* `cleanup`: Drop multiple Streamlit applications...
* `new-connection`: Add a new Snowflake connection configuration.

## `deploy`

Deploy a Streamlit application using the Snowflake CLI.

This command wraps the `snow streamlit deploy` command, providing a convenient
interface for deploying Streamlit applications to Snowflake.

By default, opens the app in your browser. Use --no-open to disable.

**Usage**:

```console
$ deploy [OPTIONS]
```

**Options**:

* `-v, --verbose`: Enable verbose output
* `-r, --replace`: Replace the Streamlit app if it already exists
* `--no-open`: Don&#x27;t open the deployed Streamlit app in a browser
* `-c, --connection TEXT`: Connection to use for deployment
* `--query-warehouse TEXT`: Override the query warehouse to use
* `--app-warehouse TEXT`: Override the app warehouse to use
* `--debug`: Enable debug output
* `--help`: Show this message and exit.

## `deploy-preview`

Deploy a preview version of a Streamlit application.

This command adds &#x27;preview_&#x27; to the beginning of the app name and also adds
&#x27;PREVIEW: &#x27; to the app title, making it easy to identify preview deployments.

By default, opens the app in your browser. Use --no-open to disable.

**Usage**:

```console
$ deploy-preview [OPTIONS]
```

**Options**:

* `--preview-name TEXT`: Name of the preview app
* `-v, --verbose`: Enable verbose output
* `-r, --replace`: Replace the Streamlit app if it already exists
* `--no-open`: Don&#x27;t open the deployed Streamlit app in a browser
* `-c, --connection TEXT`: Connection to use for deployment
* `--debug`: Enable debug output
* `--help`: Show this message and exit.

## `drop`

Drop a Streamlit application from Snowflake.

This command will remove the Streamlit app. If --drop-spcs is specified,
it will also clean up any associated SPCS services.

**Usage**:

```console
$ drop [OPTIONS]
```

**Options**:

* `-v, --verbose`: Enable verbose output
* `-c, --connection TEXT`: Connection to use for deployment
* `-f, --force`: Force drop without confirmation
* `--drop-spcs`: Also drop any associated SPCS services
* `--help`: Show this message and exit.

## `drop-preview`

Drop a preview version of a Streamlit application from Snowflake.

This command will remove the preview Streamlit app (with prefix &#x27;preview_&#x27;).
If --drop-spcs is specified, it will also clean up any associated SPCS services.

**Usage**:

```console
$ drop-preview [OPTIONS]
```

**Options**:

* `-v, --verbose`: Enable verbose output
* `-c, --connection TEXT`: Connection to use for deployment
* `-f, --force`: Force drop without confirmation
* `--drop-spcs`: Also drop any associated SPCS services
* `--help`: Show this message and exit.

## `new`

Create a new Streamlit in Snowflake application using a template.

This command uses snow init to generate a new app from the appropriate template
based on your compute choice (warehouse or compute pool).

All configuration can be provided via command line flags for automation, or
will be prompted for interactively if not provided.

**Usage**:

```console
$ new [OPTIONS] [OUTPUT_DIR]
```

**Arguments**:

* `[OUTPUT_DIR]`: Directory where the new app will be created

**Options**:

* `-f, --force`: Force creation of app, overwriting existing directory
* `-c, --connection TEXT`: Name of the connection to use
* `-v, --verbose`: Enable verbose output
* `-t, --compute-type TEXT`: Type of compute to use: &#x27;warehouse&#x27; or &#x27;compute_pool&#x27;  [default: warehouse]
* `-q, --query-warehouse TEXT`: Warehouse to use for queries (when using warehouse compute type)
* `-a, --app-warehouse TEXT`: Warehouse to use for running the app (when using warehouse compute type)
* `--compute-pool TEXT`: Compute pool to use (when using compute_pool compute type)
* `--stage TEXT`: Stage to use for app artifacts
* `--database TEXT`: Database to use for the app
* `--schema TEXT`: Schema to use for the app
* `--role TEXT`: Role to use for the app
* `--debug`: Enable debug output
* `--help`: Show this message and exit.

## `run`

Run a Streamlit application locally.

This command wraps the `streamlit run` command, providing a convenient
interface for running Streamlit applications during development.

**Usage**:

```console
$ run [OPTIONS] [APP_PATH]
```

**Arguments**:

* `[APP_PATH]`: Path to the Streamlit app file to run  [default: streamlit_app.py]

**Options**:

* `--help`: Show this message and exit.

## `test`

Run the tests for the CLI.

**Usage**:

```console
$ test [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cleanup`

Drop multiple Streamlit applications containing the specified filter text.

If no filter is provided, uses the text &#x27;preview_&#x27; as the filter.
This is useful for cleaning up development apps in your account.

**Usage**:

```console
$ cleanup [OPTIONS] [FILTER_TEXT]
```

**Arguments**:

* `[FILTER_TEXT]`: Text to filter apps by (uses preview_ if not specified)

**Options**:

* `-v, --verbose`: Enable verbose output
* `-c, --connection TEXT`: Connection to use for deployment
* `-f, --force`: Force cleanup without confirmation
* `--drop-spcs`: Also drop any associated SPCS services
* `--help`: Show this message and exit.

## `new-connection`

Add a new Snowflake connection configuration.

This command wraps the `snow connection add` command, providing a convenient
interface for adding new Snowflake connections.

**Usage**:

```console
$ new-connection [OPTIONS]
```

**Options**:

* `-n, --connection-name TEXT`: Name of the new connection.
* `-a, --account, --accountname TEXT`: Account name to use when authenticating with Snowflake.
* `-u, --user, --username TEXT`: Username to connect to Snowflake.
* `-p, --password TEXT`: Snowflake password.
* `-r, --role, --rolename TEXT`: Role to use on Snowflake.
* `-w, --warehouse TEXT`: Warehouse to use on Snowflake.
* `-d, --database, --dbname TEXT`: Database to use on Snowflake.
* `-s, --schema, --schemaname TEXT`: Schema to use on Snowflake.
* `-h, --host TEXT`: Host name the connection attempts to connect to Snowflake.
* `-P, --port INTEGER`: Port to communicate with on the host.
* `-R, --region TEXT`: Region name if not the default Snowflake deployment.
* `-A, --authenticator TEXT`: Chosen authenticator, if other than password-based
* `-k, --private-key, --private-key-file, --private-key-path TEXT`: Path to file containing private key
* `-t, --token-file-path TEXT`: Path to file with an OAuth token that should be used when connecting to Snowflake
* `--default`: If provided the connection will be configured as default connection.
* `-v, --verbose`: Enable verbose output
* `--debug`: Enable debug output
* `--help`: Show this message and exit.


<!-- [[[end]]] -->

## Configuration

`sisx` uses the `snowflake.yml` file in your project directory for configuration. This defines your app's name, database, schema, and other settings.

Example `snowflake.yml` for warehouse compute type:

```yaml
definition_version: "2"
env:
  name: "my_app"
  query_warehouse: "compute_wh"
  app_warehouse: "SYSTEM$STREAMLIT_NOTEBOOK_WH"
  schema: "public"
  database: "streamlit"
  role: "ACCOUNTADMIN"
  preview_database: "streamlit"
  preview_schema: "public"
  preview_role: "ACCOUNTADMIN"
  stage: "streamlit_stage"
entities:
  streamlit_app:
    type: streamlit
    identifier:
      name: <% ctx.env.name %>
      schema: <% ctx.env.schema %>
      database: <% ctx.env.database %>
    stage: <% ctx.env.stage %>
    query_warehouse: <% ctx.env.query_warehouse %>
    main_file: streamlit_app.py
    pages_dir: pages/
    artifacts:
      - "**/*.py"
      - "*.yml"
```

Example `snowflake.yml` for compute pool type:

```yaml
definition_version: "2"
env:
  name: "my_app"
  compute_pool: "streamlit_compute_pool"
  schema: "public"
  database: "streamlit"
  preview_database: "streamlit"
  preview_schema: "public"
  preview_role: "ACCOUNTADMIN"
  stage: "streamlit_stage"
entities:
  streamlit_app:
    type: streamlit
    identifier:
      name: <% ctx.env.name %>
      schema: <% ctx.env.schema %>
      database: <% ctx.env.database %>
    stage: <% ctx.env.stage %>
    compute_pool: <% ctx.env.compute_pool %>
    main_file: streamlit_app.py
    pages_dir: pages/
    artifacts:
      - "**/*.py"
      - "requirements.txt"
      - "*.yml"
```

## Version Information

You can check the version of sisx by running:

```bash
uvx sisx --version
```

## License

MIT
