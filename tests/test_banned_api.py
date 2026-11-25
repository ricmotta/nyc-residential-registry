"""ruff's banned-api rules (TID251) keep boto3, psycopg and httpx in their own modules.

Each case lints a snippet as if it lived at a given path in the repository, using the
project's ruff configuration, so per-file-ignores apply exactly as in CI.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def lint(source: str, path: str) -> str:
    """ruff's findings for `source` linted as if it were the file at `path`."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--no-cache",
            "--output-format",
            "concise",
            "--stdin-filename",
            path,
            "-",
        ],
        input=source,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"ruff failed to run: {result.stderr}")
    return result.stdout


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("import boto3\n", "use nyc_registry.storage"),
        ("from boto3 import client\n", "use nyc_registry.storage"),
        ("import botocore.exceptions\n", "use nyc_registry.storage"),
        ("import psycopg\n", "use nyc_registry.db"),
        ("from psycopg import connect\n", "use nyc_registry.db"),
        ("import httpx\n", "ADR 0006"),
    ],
)
def test_import_outside_its_module_fails_with_guidance(source: str, message: str) -> None:
    output = lint(source, "src/nyc_registry/somewhere.py")
    assert "TID251" in output
    assert message in output


@pytest.mark.parametrize(
    ("source", "path"),
    [
        ("import boto3\nimport botocore\n", "src/nyc_registry/storage.py"),
        ("import psycopg\n", "src/nyc_registry/db.py"),
    ],
)
def test_import_in_its_own_module_is_allowed(source: str, path: str) -> None:
    output = lint(source, path)
    assert "F401" in output  # ruff did lint the snippet
    assert "TID251" not in output


def test_the_temporary_httpx_exception_does_not_cover_the_whole_smoke_module() -> None:
    output = lint("import psycopg\n", "src/nyc_registry/smoke.py")
    assert "use nyc_registry.db" in output
