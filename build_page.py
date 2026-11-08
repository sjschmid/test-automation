#!/usr/bin/env python3
"""Build index.html visualizing the newest weather report in weather/."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
WMO = {
    0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"), 45: ("Fog", "🌫️"), 48: ("Rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"), 53: ("Drizzle", "🌦️"), 55: ("Dense drizzle", "🌧️"),
    61: ("Light rain", "🌧️"), 63: ("Rain", "🌧️"), 65: ("Heavy rain", "🌧️"),
    71: ("Light snow", "🌨️"), 73: ("Snow", "🌨️"), 75: ("Heavy snow", "❄️"),
    80: ("Rain showers", "🌦️"), 81: ("Rain showers", "🌧️"), 82: ("Violent showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm, hail", "⛈️"), 99: ("Thunderstorm, hail", "⛈️"),
}


def parse(path: Path) -> dict:
    d = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        k, _, v = line.partition(": ")
        d[k] = v
    return d


def num(s: str) -> float:
    return float(re.match(r"-?[\d.]+", s).group())


def main() -> None:
    files = sorted(ROOT.glob("weather/weather-in-stuttgart_*.txt"))
    if not files:
        raise SystemExit("No weather files found.")
    d = parse(files[-1])
    temp, feels = num(d["Temperature"]), num(d["Feels like"])
    hum, wind, rain = num(d["Humidity"]), num(d["Wind speed"]), num(d["Precipitation"])
    label, icon = WMO.get(int(d["WMO weather code"]), ("Unknown", "🌡️"))
    # thermometer fill: -10..35 °C mapped to 0..100 %
    fill = max(0, min(100, (temp + 10) / 45 * 100))
    e = html.escape
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Weather in Stuttgart</title>
<style>
:root{{--bg:#eef3f8;--card:#fff;--text:#18222d;--muted:#667585;--accent:#2f7de1;--track:#dde6ef}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0f1720;--card:#18232f;--text:#e8eef4;--muted:#8fa1b3;--accent:#5aa2ff;--track:#2a3948}}}}
*{{box-sizing:border-box}}
body{{margin:0;padding:24px 16px;background:var(--bg);color:var(--text);font:16px/1.4 system-ui,sans-serif}}
main{{max-width:560px;margin:0 auto}}
h1{{font-size:1rem;font-weight:600;color:var(--muted);margin:0 0 12px}}
.card{{background:var(--card);border-radius:16px;padding:20px;box-shadow:0 1px 4px #0002}}
.hero{{display:flex;align-items:center;gap:16px}}
.icon{{font-size:64px;line-height:1}}
.temp{{font-size:3.5rem;font-weight:700;line-height:1}}
.cond{{color:var(--muted)}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}}
.m .v{{font-size:1.5rem;font-weight:600}}.m .l{{color:var(--muted);font-size:.85rem}}
.bar{{height:8px;border-radius:4px;background:var(--track);margin-top:8px;overflow:hidden}}
.bar i{{display:block;height:100%;background:var(--accent);border-radius:4px}}
.foot{{color:var(--muted);font-size:.8rem;margin-top:16px;text-align:center}}
</style></head><body><main>
<h1>Weather in Stuttgart, Germany</h1>
<div class="card hero"><div class="icon">{icon}</div>
<div><div class="temp">{temp:g}°C</div><div class="cond">{e(label)} · feels like {feels:g}°C</div></div></div>
<div class="grid">
<div class="card m"><div class="v">{hum:g} %</div><div class="l">Humidity</div><div class="bar"><i style="width:{hum:g}%"></i></div></div>
<div class="card m"><div class="v">{wind:g} km/h</div><div class="l">Wind speed</div><div class="bar"><i style="width:{min(100, wind / 60 * 100):.0f}%"></i></div></div>
<div class="card m"><div class="v">{rain:g} mm</div><div class="l">Precipitation</div><div class="bar"><i style="width:{min(100, rain / 10 * 100):.0f}%"></i></div></div>
<div class="card m"><div class="v">{temp:g}°C</div><div class="l">Temperature (-10 to 35 °C)</div><div class="bar"><i style="width:{fill:.0f}%"></i></div></div>
</div>
<div class="foot">Observed {e(d["Observation time (UTC)"])} UTC · source: {e(files[-1].name)}</div>
</main></body></html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("Wrote index.html")


if __name__ == "__main__":
    main()
