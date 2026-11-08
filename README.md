# test-automation

`fetch_weather.py` pulls the current weather in Stuttgart from Open-Meteo and writes it to
`weather/weather-in-stuttgart_<datetime>.txt`. The GitHub Actions workflow runs it on every push
to `main`/`master` and commits the new file back.
