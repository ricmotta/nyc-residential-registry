"""The smoke check reports every check and fails when any one fails."""

from nyc_registry.config import Settings
from nyc_registry.smoke import run_checks

SETTINGS = Settings(
    registry_db_name="registry",
    registry_db_user="registry",
    registry_db_password="pw-value-123",  # type: ignore[arg-type]
    s3_endpoint_url="http://localhost:8333",
    s3_access_key="key",  # type: ignore[arg-type]
    s3_secret_key="sk-value-456",  # type: ignore[arg-type]
    _env_file=None,  # type: ignore[call-arg]
)


def passing(_: Settings) -> str:
    return "fine"


def failing(_: Settings) -> str:
    raise ConnectionError("refused")


def test_all_checks_pass() -> None:
    results = run_checks(SETTINGS, {"a": passing, "b": passing})
    assert [r.ok for r in results] == [True, True]


def test_a_failing_check_is_reported_and_does_not_hide_the_others() -> None:
    results = run_checks(SETTINGS, {"a": failing, "b": passing})
    assert [(r.name, r.ok) for r in results] == [("a", False), ("b", True)]
    assert results[0].detail == "ConnectionError: refused"


def test_secrets_are_not_shown_in_settings_repr() -> None:
    assert "pw-value-123" not in repr(SETTINGS)
    assert "sk-value-456" not in repr(SETTINGS)
