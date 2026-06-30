"""Transform: normalise raw Open-Meteo payloads into flat snapshot records."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from .capitals import Capital

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WeatherRecord:
    snapshot_id: UUID
    snapshot_at: datetime
    capital: str
    country: str
    latitude: float
    longitude: float
    temperature_c: float | None
    wind_speed_kmh: float | None
    wind_direction_deg: float | None
    humidity_pct: float | None
    sunrise: datetime | None
    sunset: datetime | None
    observed_at: datetime | None


def _parse_local_iso(value: str | None, utc_offset_seconds: int | None) -> datetime | None:
    """Parse an Open-Meteo local timestamp into a timezone-aware datetime.

    Open-Meteo returns naive local times (because timezone=auto) plus a
    ``utc_offset_seconds`` field describing that locale, so we attach it.
    """
    if not value:
        return None
    naive = datetime.fromisoformat(value)
    if utc_offset_seconds is None:
        return naive.replace(tzinfo=timezone.utc)
    tz = timezone.utc if utc_offset_seconds == 0 else _fixed_offset(utc_offset_seconds)
    return naive.replace(tzinfo=tz)


def _fixed_offset(seconds: int):
    from datetime import timedelta

    return timezone(timedelta(seconds=seconds))


def _first(value):
    """Open-Meteo daily fields are 1-element lists; pull the first element."""
    if isinstance(value, list):
        return value[0] if value else None
    return value


def to_record(
    capital: Capital, raw: dict, snapshot_id: UUID, snapshot_at: datetime
) -> WeatherRecord:
    current = raw.get("current") or {}
    daily = raw.get("daily") or {}
    offset = raw.get("utc_offset_seconds")

    return WeatherRecord(
        snapshot_id=snapshot_id,
        snapshot_at=snapshot_at,
        capital=capital.name,
        country=capital.country,
        latitude=capital.latitude,
        longitude=capital.longitude,
        temperature_c=current.get("temperature_2m"),
        wind_speed_kmh=current.get("wind_speed_10m"),
        wind_direction_deg=current.get("wind_direction_10m"),
        humidity_pct=current.get("relative_humidity_2m"),
        sunrise=_parse_local_iso(_first(daily.get("sunrise")), offset),
        sunset=_parse_local_iso(_first(daily.get("sunset")), offset),
        observed_at=_parse_local_iso(current.get("time"), offset),
    )


def transform_all(
    pairs: list[tuple[Capital, dict]], snapshot_id: UUID, snapshot_at: datetime
) -> list[WeatherRecord]:
    records: list[WeatherRecord] = []
    for capital, raw in pairs:
        try:
            records.append(to_record(capital, raw, snapshot_id, snapshot_at))
        except Exception:  # noqa: BLE001 - one bad city shouldn't sink the run
            logger.exception("Failed to transform payload for %s", capital.name)
    return records
