"""The only module that imports psycopg: database connections come from Settings."""

import psycopg
from psycopg.rows import TupleRow

from nyc_registry.config import Settings


def connect(settings: Settings, *, connect_timeout: int) -> psycopg.Connection[TupleRow]:
    """A connection to the project database (PostgreSQL + PostGIS, ADR 0002)."""
    return psycopg.connect(settings.postgres_conninfo(), connect_timeout=connect_timeout)
