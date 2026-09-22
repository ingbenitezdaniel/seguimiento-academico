import pytest

from academic_tracking.config import DatabaseSettings


def test_database_settings_are_loaded_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POSTGRES_HOST", "database.example")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    monkeypatch.setenv("POSTGRES_DB", "academic_database")
    monkeypatch.setenv("POSTGRES_USER", "test_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test_password")

    settings = DatabaseSettings.from_environment()

    assert settings == DatabaseSettings(
        host="database.example",
        port=5433,
        dbname="academic_database",
        user="test_user",
        password="test_password",
    )


def test_database_settings_require_a_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    with pytest.raises(
        RuntimeError,
        match="Set POSTGRES_PASSWORD before starting the application",
    ):
        DatabaseSettings.from_environment()


def test_database_settings_use_local_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("POSTGRES_HOST", raising=False)
    monkeypatch.delenv("POSTGRES_PORT", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.setenv("POSTGRES_PASSWORD", "test_password")

    settings = DatabaseSettings.from_environment()

    assert settings == DatabaseSettings(
        host="127.0.0.1",
        port=55432,
        dbname="academic_tracking",
        user="academic_user",
        password="test_password",
    )
