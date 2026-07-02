"""Entry point: run one full ETL cycle producing a single weather snapshot."""

from __future__ import annotations

import argparse
import logging
import time
from datetime import datetime, timezone
from uuid import uuid4

from .capitals import EUROPEAN_CAPITALS
from .db import connect
from .extract import fetch_weather
from .load import load_snapshot
from .migrate import run_migrations
from .transform import transform_all

logger = logging.getLogger(__name__)


def run(skip_migrations: bool = False) -> int:
    """Execute extract -> transform -> load. Returns rows inserted."""
    snapshot_id = uuid4()
    snapshot_at = datetime.now(timezone.utc)
    logger.info("Starting snapshot %s at %s", snapshot_id, snapshot_at.isoformat())

    with connect() as conn:
        if not skip_migrations:
            run_migrations(conn)

        pairs = fetch_weather(list(EUROPEAN_CAPITALS))
        records = transform_all(pairs, snapshot_id, snapshot_at)

        # Emulate long-running work.
        logger.info("Simulating long-running work for 60s...")
        time.sleep(60)

        inserted = load_snapshot(conn, records)

    logger.info("Snapshot %s complete: %d rows.", snapshot_id, inserted)
    return inserted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-migrations",
        action="store_true",
        help="Do not run pending migrations before loading.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Python logging level (default: INFO).",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    run(skip_migrations=args.skip_migrations)


if __name__ == "__main__":
    main()
