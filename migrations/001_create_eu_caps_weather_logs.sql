-- Snapshot table: each ETL run inserts one row per European capital, all
-- sharing the same snapshot_id and snapshot_at. Querying by snapshot_id (or
-- ordering by snapshot_at) gives you a point-in-time view of the continent.

CREATE TABLE IF NOT EXISTS eu_caps_weather_logs (
    id                  BIGSERIAL       PRIMARY KEY,
    snapshot_id         UUID            NOT NULL,
    snapshot_at         TIMESTAMPTZ     NOT NULL,
    capital             TEXT            NOT NULL,
    country             TEXT            NOT NULL,
    latitude            DOUBLE PRECISION NOT NULL,
    longitude           DOUBLE PRECISION NOT NULL,
    temperature_c       DOUBLE PRECISION,
    wind_speed_kmh      DOUBLE PRECISION,
    wind_direction_deg  DOUBLE PRECISION,
    humidity_pct        DOUBLE PRECISION,
    sunrise             TIMESTAMPTZ,
    sunset              TIMESTAMPTZ,
    observed_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_eu_caps_weather_logs_snapshot_id
    ON eu_caps_weather_logs (snapshot_id);

CREATE INDEX IF NOT EXISTS ix_eu_caps_weather_logs_snapshot_at
    ON eu_caps_weather_logs (snapshot_at);

CREATE INDEX IF NOT EXISTS ix_eu_caps_weather_logs_capital
    ON eu_caps_weather_logs (capital);
