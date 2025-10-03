"""
Weather and Soil data utilities for CropSense UI
"""
import datetime as _dt
from typing import Dict, Optional, Tuple
import requests

_WEATHER_CACHE: Dict[Tuple[float, float, str, str], Dict] = {}
_SOIL_CACHE: Dict[Tuple[float, float], Dict] = {}


def _date_str(d: _dt.date | _dt.datetime) -> str:
    if isinstance(d, _dt.datetime):
        return d.date().isoformat()
    return d.isoformat()


def fetch_weather(latitude: float, longitude: float, start_date: _dt.date, end_date: _dt.date) -> Optional[Dict]:
    """Fetch aggregated weather from Open-Meteo and return mean temperature and total rainfall.

    Returns dict: { "Temperature_Celsius": float, "Rainfall_mm": float }
    """
    s, e = _date_str(start_date), _date_str(end_date)
    key = (round(latitude, 4), round(longitude, 4), s, e)
    if key in _WEATHER_CACHE:
        return _WEATHER_CACHE[key]

    base = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "start_date": s,
        "end_date": e,
        "timezone": "UTC",
    }
    try:
        r = requests.get(base, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        hourly = data.get("hourly", {})
        temps = hourly.get("temperature_2m", [])
        precs = hourly.get("precipitation", [])
        if not temps:
            return None
        temp_mean = sum(temps) / max(1, len(temps))
        rain_total = float(sum(precs)) if precs else 0.0
        result = {"Temperature_Celsius": float(temp_mean), "Rainfall_mm": float(rain_total)}
        _WEATHER_CACHE[key] = result
        return result
    except Exception:
        return None


def fetch_soil(latitude: float, longitude: float) -> Optional[Dict]:
    """Fetch soil properties from SoilGrids (approximate pH and organic carbon).

    Returns dict: { "soil_ph": float | None, "organic_matter": float | None }
    """
    key = (round(latitude, 4), round(longitude, 4))
    if key in _SOIL_CACHE:
        return _SOIL_CACHE[key]

    base = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    params = {
        "lat": latitude,
        "lon": longitude,
        "property": "phh2o,ocd",
        "depth": "0-5cm",
    }
    try:
        r = requests.get(base, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Extract simple estimates if available
        ph = None
        oc = None
        props = data.get("properties", {}).get("layers", [])
        for layer in props:
            name = layer.get("name")
            vals = layer.get("depths", [])
            if not vals:
                continue
            stats = vals[0].get("values", {})
            mean = stats.get("mean")
            if mean is None:
                continue
            if name == "phh2o":
                # phh2o reported as pH * 10 in some products; clamp to plausible range
                v = float(mean)
                ph = v / 10.0 if v > 14 else v
            if name == "ocd":
                oc = float(mean)

        result = {"soil_ph": ph, "organic_matter": oc}
        _SOIL_CACHE[key] = result
        return result
    except Exception:
        return None


