"""Placeholder test proving the test pipeline runs end to end."""

import nyc_registry


def test_package_exposes_a_version() -> None:
    assert nyc_registry.__version__ == "0.1.0"

import os
