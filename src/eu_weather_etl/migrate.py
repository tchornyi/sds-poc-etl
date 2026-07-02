"""A minimal forward-only SQL migration runner.

Migrations live in the top-level ``migrations/`` directory as ``*.sql`` files
named with a sortable numeric prefix (e.g. ``001_...sql``). Applied versions are
tracked in the ``schema_migrations`` table so each file runs exactly once.
"""

from __future__ import annotations

import logging
from pathlib import Path

import psycopg

from eu_weather_etl.db import connect

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"

_TRACKING_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version     TEXT        PRIMARY KEY,
    applied_at  TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""


def _discover_migrations() -> list[Path]:
    if not MIGRATIONS_DIR.is_dir():
        raise RuntimeError(f"Migrations directory not found: {MIGRATIONS_DIR}")
    return sorted(MIGRATIONS_DIR.glob("*.sql"))


def _applied_versions(conn: psycopg.Connection) -> set[str]:
    with conn.cursor() as cur:
        cur.execute("SELECT version FROM schema_migrations")
        return {row[0] for row in cur.fetchall()}


def run_migrations(conn: psycopg.Connection | None = None) -> int:
    """Apply any pending migrations. Returns the number of files applied."""
    owns_connection = conn is None
    conn = conn or connect()
    applied = 0
    try:
        with conn.cursor() as cur:
            cur.execute(_TRACKING_TABLE_DDL)
        conn.commit()

        done = _applied_versions(conn)
        for path in _discover_migrations():
            version = path.stem
            if version in done:
                logger.debug("Skipping already-applied migration %s", version)
                continue

            logger.info("Applying migration %s", version)
            sql = path.read_text(encoding="utf-8")
            # Each migration runs in its own transaction so a failure leaves
            # the database in a consistent, partially-migrated-but-clean state.
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(sql)
                    cur.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s)",
                        (version,),
                    )
            applied += 1

        if applied:
            logger.info("Applied %d migration(s).", applied)
        else:
            logger.info("Database schema already up to date.")
        return applied
    finally:
        if owns_connection:
            conn.close()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    run_migrations()


if __name__ == "__main__":
    main()
