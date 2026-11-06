---
name: open-meteo-weather
description: "Weather now and daily forecast from Open-Meteo; no API key"
version: 1.0.0
author: earl-kayy
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Weather, Forecast, Open-Meteo, Briefing]
    category: productivity
---

# Open-Meteo Weather

Current conditions and a daily forecast (high and low, rain chance and amount, wind) for a place name or coordinates, from the free Open-Meteo API. The script, `scripts/weather.py`, is standard-library Python 3: no API key, nothing to install.

## When to use

- The user asks about the weather, the temperature, rain, or whether to bring an umbrella.
- A morning briefing or a day plan needs today's weather.

## How to run

```bash
python3 ${HERMES_SKILL_DIR}/scripts/weather.py "Los Angeles, CA" --days 1 --units imperial
```

- The place is a city name, optionally followed by a state or country after a comma ("Paris, France", "Springfield, IL"). Or pass `--lat 34.05 --lon -118.24` instead of a name.
- `--days N`: forecast days, 1 to 16 (default 3). Use 1 for today only.
- `--units imperial` gives °F, mph, and inches; `--units metric` (the default) gives °C, km/h, and mm. Use the user's preferred units.
- Run it as one plain command in exactly this form, with nothing piped or chained to it.

## Output

```
Los Angeles, California, United States (34.05, -118.24), time zone America/Los_Angeles
Now (1:45 AM): 58°F, Overcast, wind 5 mph
Thu, Nov 5: Overcast, high 82°F, low 57°F, rain chance 0% (0.00 in), wind up to 10 mph
Weather data by Open-Meteo.com (CC BY 4.0, https://open-meteo.com/); location data based on GeoNames.
```

Check the place on the first line. If it's the wrong one, run again with a state or country added.

Whenever you show weather from this skill, end with the line "Weather data by Open-Meteo.com". Open-Meteo's licence (CC BY 4.0) requires that credit next to the data.

## Limits

Open-Meteo's free API is for non-commercial use, under 10,000 calls a day. If the script fails, say that the weather is unavailable and why; never guess a forecast.
