"""Runtime configuration, sourced entirely from environment variables."""

from __future__ import annotations

import os

from dotenv import load_dotenv

# Load a local .env file if present. Real environment variables always win,
# because load_dotenv does not override values that are already set.
load_dotenv()


def database_connection_kwargs() -> dict[str, object]:
    """Build the keyword arguments for psycopg.connect from the environment.

    If DATABASE_URL is set it is used verbatim as a libpq connection string.
    Otherwise the standard PG* variables are assembled into a connection.
    """
    url = os.environ.get("DATABASE_URL")
    if url:
        return {"conninfo": url}

    missing = [
        name
        for name in ("PGHOST", "PGDATABASE", "PGUSER")
        if not os.environ.get(name)
    ]
    if missing:
        raise RuntimeError(
            "Missing database configuration. Set DATABASE_URL, or provide "
            f"these environment variables: {', '.join(missing)}. "
            "See .env.example for the full list."
        )

    kwargs: dict[str, object] = {
        "host": os.environ["PGHOST"],
        "dbname": os.environ["PGDATABASE"],
        "user": os.environ["PGUSER"],
    }
    if os.environ.get("PGPORT"):
        kwargs["port"] = int(os.environ["PGPORT"])
    if os.environ.get("PGPASSWORD"):
        kwargs["password"] = os.environ["PGPASSWORD"]
    if os.environ.get("PGSSLMODE"):
        kwargs["sslmode"] = os.environ["PGSSLMODE"]
    return kwargs
