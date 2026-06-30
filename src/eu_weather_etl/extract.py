"""Extract: fetch current weather for every capital from the Open-Meteo API.

Open-Meteo (https://open-meteo.com) is free for non-commercial use and needs no
API key. It accepts comma-separated coordinate lists, so a whole batch of
capitals is retrieved in a single HTTP request.
"""

from __future__ import annotations

import logging

import httpx

from .capitals import Capital

logger = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"
# Keep batches comfortably under URL-length limits.
BATCH_SIZE = 20
REQUEST_TIMEOUT = 30.0

_CURRENT_FIELDS = "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m"
_DAILY_FIELDS = "sunrise,sunset"


def _request_batch(client: httpx.Client, batch: list[Capital]) -> list[dict]:
    params = {
        "latitude": ",".join(str(c.latitude) for c in batch),
        "longitude": ",".join(str(c.longitude) for c in batch),
        "current": _CURRENT_FIELDS,
        "daily": _DAILY_FIELDS,
        "wind_speed_unit": "kmh",
        "timezone": "auto",
        "forecast_days": 1,
    }
    response = client.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    # The API returns a bare object for a single location and a list for many.
    return payload if isinstance(payload, list) else [payload]


def fetch_weather(capitals: list[Capital]) -> list[tuple[Capital, dict]]:
    """Return (capital, raw_api_result) pairs for each requested capital."""
    results: list[tuple[Capital, dict]] = []
    with httpx.Client(headers={"User-Agent": "eu-weather-etl/0.1"}) as client:
        for start in range(0, len(capitals), BATCH_SIZE):
            batch = capitals[start : start + BATCH_SIZE]
            logger.info(
                "Fetching weather for %d capitals (%d-%d of %d)",
                len(batch),
                start + 1,
                start + len(batch),
                len(capitals),
            )
            for capital, raw in zip(batch, _request_batch(client, batch)):
                results.append((capital, raw))
    return results
