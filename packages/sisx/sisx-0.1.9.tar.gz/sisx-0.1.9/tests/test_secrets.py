from sisx.utils.secrets import _get_connection_settings, create_secrets_file


def test_create_secrets_file_warehouse(tmp_path):
    """Test creating secrets file with warehouse configuration."""
    connection_config = {
        "parameters": {
            "account": "test_account",
            "user": "test_user",
            "password": "test_password",
            "role": "test_role",
            "database": "test_db",
            "schema": "test_schema",
            "warehouse": "test_warehouse",
        }
    }
    compute_config = {"type": "warehouse", "app_warehouse": "test_app_warehouse"}

    create_secrets_file(tmp_path, connection_config, compute_config)

    secrets_path = tmp_path / ".streamlit" / "secrets.toml"
    assert secrets_path.exists()

    content = secrets_path.read_text()
    assert "[connections.snowflake]" in content
    assert 'account = "test_account"' in content
    assert 'user = "test_user"' in content
    assert 'password = "test_password"' in content
    assert 'role = "test_role"' in content
    assert 'database = "test_db"' in content
    assert 'schema = "test_schema"' in content
    assert 'warehouse = "test_app_warehouse"' in content


def test_create_secrets_file_compute_pool(tmp_path):
    """Test creating secrets file with compute pool configuration."""
    connection_config = {
        "parameters": {
            "account": "test_account",
            "user": "test_user",
            "authenticator": "externalbrowser",
            "database": "test_db",
            "schema": "test_schema",
        }
    }
    compute_config = {"type": "compute_pool", "compute_pool": "test_compute_pool"}

    create_secrets_file(tmp_path, connection_config, compute_config)

    secrets_path = tmp_path / ".streamlit" / "secrets.toml"
    assert secrets_path.exists()

    content = secrets_path.read_text()
    assert "[connections.snowflake]" in content
    assert 'account = "test_account"' in content
    assert 'user = "test_user"' in content
    assert 'authenticator = "externalbrowser"' in content
    assert 'database = "test_db"' in content
    assert 'schema = "test_schema"' in content
    assert 'compute_pool = "test_compute_pool"' in content
    assert "warehouse" not in content


def test_get_connection_settings_warehouse():
    """Test _get_connection_settings with warehouse configuration."""
    connection_config = {
        "account": "test_account",
        "user": "test_user",
        "password": "test_password",
        "role": "test_role",
        "database": "test_db",
        "schema": "test_schema",
        "warehouse": "test_warehouse",
        "ignored_key": "should_not_appear",
    }
    compute_config = {"type": "warehouse", "app_warehouse": "test_app_warehouse"}

    settings = _get_connection_settings(connection_config, compute_config)

    assert settings["account"] == "test_account"
    assert settings["user"] == "test_user"
    assert settings["password"] == "test_password"
    assert settings["role"] == "test_role"
    assert settings["database"] == "test_db"
    assert settings["schema"] == "test_schema"
    assert settings["warehouse"] == "test_app_warehouse"
    assert "ignored_key" not in settings


def test_get_connection_settings_compute_pool():
    """Test _get_connection_settings with compute pool configuration."""
    connection_config = {
        "account": "test_account",
        "user": "test_user",
        "authenticator": "externalbrowser",
        "database": "test_db",
        "schema": "test_schema",
        "warehouse": "should_not_appear",
    }
    compute_config = {"type": "compute_pool", "compute_pool": "test_compute_pool"}

    settings = _get_connection_settings(connection_config, compute_config)

    assert settings["account"] == "test_account"
    assert settings["user"] == "test_user"
    assert settings["authenticator"] == "externalbrowser"
    assert settings["database"] == "test_db"
    assert settings["schema"] == "test_schema"
    assert settings["compute_pool"] == "test_compute_pool"
    assert "warehouse" not in settings


def test_get_connection_settings_skip_invalid():
    """Test _get_connection_settings skips invalid values."""
    connection_config = {
        "account": "test_account",
        "password": "****",  # Should be skipped
        "role": None,  # Should be skipped
        "database": 123,  # Should be skipped (not a string)
    }
    compute_config = {"type": "warehouse", "app_warehouse": "test_app_warehouse"}

    settings = _get_connection_settings(connection_config, compute_config)

    assert settings["account"] == "test_account"
    assert settings["warehouse"] == "test_app_warehouse"
    assert "password" not in settings
    assert "role" not in settings
    assert "database" not in settings
