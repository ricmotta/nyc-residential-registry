"""Smoke check for the local environment.

Run with `uv run python -m nyc_registry.smoke`. Exits 0 only if every check passes:
PostGIS is installed, the Bronze bucket accepts a put/get through the S3 API,
Airflow's API server reports healthy, and `dbt debug` passes.
"""

import subprocess
import sys
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

# Temporary exception, scoped to this line: moves to the collector HTTP client (#15).
import httpx  # noqa: TID251

from nyc_registry.config import Settings
from nyc_registry.db import connect
from nyc_registry.storage import ensure_bucket, s3_client

DBT_PROJECT_DIR = Path(__file__).resolve().parents[2] / "dbt"


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def check_postgis(settings: Settings) -> str:
    with connect(settings, connect_timeout=5) as conn:
        row = conn.execute(
            "SELECT postgis_lib_version(), current_setting('server_version')"
        ).fetchone()
    if row is None:
        raise RuntimeError("PostGIS version query returned no row")
    return f"PostGIS {row[0]} on PostgreSQL {row[1]}"


def check_bronze_bucket(settings: Settings) -> str:
    client = s3_client(settings)
    created = ensure_bucket(client, settings.bronze_bucket)
    key = f"_smoke/{uuid.uuid4()}.txt"
    body = b"smoke"
    client.put_object(Bucket=settings.bronze_bucket, Key=key, Body=body)
    try:
        read = client.get_object(Bucket=settings.bronze_bucket, Key=key)["Body"].read()
    finally:
        client.delete_object(Bucket=settings.bronze_bucket, Key=key)
    if read != body:
        raise RuntimeError("object read back does not match what was written")
    return f"bucket '{settings.bronze_bucket}'" + (" created" if created else " exists")


def check_airflow(settings: Settings) -> str:
    response = httpx.get(f"{settings.airflow_url}/api/v2/monitor/health", timeout=10)
    response.raise_for_status()
    health = response.json()
    unhealthy = [
        component
        for component, status in health.items()
        if isinstance(status, dict) and status.get("status") not in (None, "healthy")
    ]
    if unhealthy:
        raise RuntimeError(f"unhealthy components: {', '.join(unhealthy)}")
    return "all components healthy"


def check_dbt(_: Settings) -> str:
    result = subprocess.run(
        [
            "dbt",
            "debug",
            "--project-dir",
            str(DBT_PROJECT_DIR),
            "--profiles-dir",
            str(DBT_PROJECT_DIR),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            result.stdout.strip().splitlines()[-1] if result.stdout else result.stderr
        )
    return "dbt debug passed"


CHECKS: dict[str, Callable[[Settings], str]] = {
    "postgis": check_postgis,
    "bronze_bucket": check_bronze_bucket,
    "airflow": check_airflow,
    "dbt": check_dbt,
}


def run_checks(
    settings: Settings, checks: dict[str, Callable[[Settings], str]]
) -> list[CheckResult]:
    """Run every check and report each one; a failing check never hides the others."""
    results = []
    for name, check in checks.items():
        try:
            results.append(CheckResult(name, True, check(settings)))
        except Exception as error:  # noqa: BLE001 - reported below and turned into a non-zero exit
            results.append(CheckResult(name, False, f"{type(error).__name__}: {error}"))
    return results


def main() -> int:
    results = run_checks(Settings(), CHECKS)  # type: ignore[call-arg]
    for result in results:
        print(f"[{'ok' if result.ok else 'FAIL'}] {result.name}: {result.detail}")
    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
