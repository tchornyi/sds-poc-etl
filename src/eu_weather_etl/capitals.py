"""Static reference data: European capitals with their coordinates.

Coordinates are the approximate city centre (WGS84). This keeps the ETL fully
self-contained and deterministic — no geocoding API is required.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capital:
    name: str
    country: str
    latitude: float
    longitude: float


EUROPEAN_CAPITALS: tuple[Capital, ...] = (
    Capital("Tirana", "Albania", 41.3275, 19.8189),
    Capital("Andorra la Vella", "Andorra", 42.5063, 1.5218),
    Capital("Vienna", "Austria", 48.2082, 16.3738),
    Capital("Minsk", "Belarus", 53.9006, 27.5590),
    Capital("Brussels", "Belgium", 50.8503, 4.3517),
    Capital("Sarajevo", "Bosnia and Herzegovina", 43.8563, 18.4131),
    Capital("Sofia", "Bulgaria", 42.6977, 23.3219),
    Capital("Zagreb", "Croatia", 45.8150, 15.9819),
    Capital("Nicosia", "Cyprus", 35.1856, 33.3823),
    Capital("Prague", "Czechia", 50.0755, 14.4378),
    Capital("Copenhagen", "Denmark", 55.6761, 12.5683),
    Capital("Tallinn", "Estonia", 59.4370, 24.7536),
    Capital("Helsinki", "Finland", 60.1699, 24.9384),
    Capital("Paris", "France", 48.8566, 2.3522),
    Capital("Berlin", "Germany", 52.5200, 13.4050),
    Capital("Athens", "Greece", 37.9838, 23.7275),
    Capital("Budapest", "Hungary", 47.4979, 19.0402),
    Capital("Reykjavik", "Iceland", 64.1466, -21.9426),
    Capital("Dublin", "Ireland", 53.3498, -6.2603),
    Capital("Rome", "Italy", 41.9028, 12.4964),
    Capital("Pristina", "Kosovo", 42.6629, 21.1655),
    Capital("Riga", "Latvia", 56.9496, 24.1052),
    Capital("Vaduz", "Liechtenstein", 47.1410, 9.5209),
    Capital("Vilnius", "Lithuania", 54.6872, 25.2797),
    Capital("Luxembourg", "Luxembourg", 49.6116, 6.1319),
    Capital("Valletta", "Malta", 35.8989, 14.5146),
    Capital("Chisinau", "Moldova", 47.0105, 28.8638),
    Capital("Monaco", "Monaco", 43.7384, 7.4246),
    Capital("Podgorica", "Montenegro", 42.4304, 19.2594),
    Capital("Amsterdam", "Netherlands", 52.3676, 4.9041),
    Capital("Skopje", "North Macedonia", 41.9981, 21.4254),
    Capital("Oslo", "Norway", 59.9139, 10.7522),
    Capital("Warsaw", "Poland", 52.2297, 21.0122),
    Capital("Lisbon", "Portugal", 38.7223, -9.1393),
    Capital("Bucharest", "Romania", 44.4268, 26.1025),
    Capital("Moscow", "Russia", 55.7558, 37.6173),
    Capital("San Marino", "San Marino", 43.9424, 12.4578),
    Capital("Belgrade", "Serbia", 44.7866, 20.4489),
    Capital("Bratislava", "Slovakia", 48.1486, 17.1077),
    Capital("Ljubljana", "Slovenia", 46.0569, 14.5058),
    Capital("Madrid", "Spain", 40.4168, -3.7038),
    Capital("Stockholm", "Sweden", 59.3293, 18.0686),
    Capital("Bern", "Switzerland", 46.9480, 7.4474),
    Capital("Kyiv", "Ukraine", 50.4501, 30.5234),
    Capital("London", "United Kingdom", 51.5074, -0.1278),
    Capital("Vatican City", "Vatican City", 41.9029, 12.4534),
)
