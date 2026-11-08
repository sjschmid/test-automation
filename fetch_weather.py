#!/usr/bin/env python3
"""Fetch the current weather in Stuttgart (Open-Meteo, no API key) and write it to a file."""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=48.7758&longitude=9.1829"
    "&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
    "precipitation,wind_speed_10m,weather_code"
    "&timezone=UTC"
)
OUT_DIR = Path(__file__).parent / "weather"


def main() -> None:
    with urllib.request.urlopen(URL, timeout=30) as resp:
        data = json.load(resp)
    cur, units = data["current"], data["current_units"]
    now = datetime.now(timezone.utc)
    lines = [
        "Weather in Stuttgart, Germany",
        f"Fetched at (UTC): {now.isoformat(timespec='seconds')}",
        f"Observation time (UTC): {cur['time']}",
        f"Temperature: {cur['temperature_2m']} {units['temperature_2m']}",
        f"Feels like: {cur['apparent_temperature']} {units['apparent_temperature']}",
        f"Humidity: {cur['relative_humidity_2m']} {units['relative_humidity_2m']}",
        f"Precipitation: {cur['precipitation']} {units['precipitation']}",
        f"Wind speed: {cur['wind_speed_10m']} {units['wind_speed_10m']}",
        f"WMO weather code: {cur['weather_code']}",
    ]
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / f"weather-in-stuttgart_{now.strftime('%Y-%m-%dT%H-%M-%S')}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
