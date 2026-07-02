"""Load: bulk-insert a batch of weather records as one snapshot."""

from __future__ import annotations

import logging

import psycopg

from eu_weather_etl.transform import WeatherRecord

logger = logging.getLogger(__name__)

_INSERT_SQL = """
INSERT INTO eu_caps_weather_logs (
    snapshot_id, snapshot_at, capital, country, latitude, longitude,
    temperature_c, wind_speed_kmh, wind_direction_deg, humidity_pct,
    sunrise, sunset, observed_at
) VALUES (
    %(snapshot_id)s, %(snapshot_at)s, %(capital)s, %(country)s, %(latitude)s,
    %(longitude)s, %(temperature_c)s, %(wind_speed_kmh)s, %(wind_direction_deg)s,
    %(humidity_pct)s, %(sunrise)s, %(sunset)s, %(observed_at)s
)
"""


def load_snapshot(conn: psycopg.Connection, records: list[WeatherRecord]) -> int:
    """Insert all records in a single transaction. Returns the row count."""
    if not records:
        logger.warning("No records to load; skipping insert.")
        return 0

    rows = [vars(record) for record in records]
    with conn.transaction():
        with conn.cursor() as cur:
            cur.executemany(_INSERT_SQL, rows)
    logger.info("Inserted %d rows into eu_caps_weather_logs.", len(rows))
    return len(rows)
