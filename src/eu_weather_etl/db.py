"""Thin database helpers built on psycopg 3."""

from __future__ import annotations

import psycopg

from eu_weather_etl.config import database_connection_kwargs


def connect() -> psycopg.Connection:
    """Open a new PostgreSQL connection using environment configuration."""
    return psycopg.connect(**database_connection_kwargs())
