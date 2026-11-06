#!/usr/bin/env python3
"""Current weather and a daily forecast from Open-Meteo, for a place name or coordinates.

  python3 weather.py "Los Angeles, CA" [--days 3] [--units imperial|metric]
  python3 weather.py --lat 34.05 --lon -118.24 [--days 3] [--units imperial|metric]

Standard library only. No API key: Open-Meteo's free API is for non-commercial use, under 10,000 calls a day.
Weather data by Open-Meteo.com (CC BY 4.0); location data based on GeoNames.
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "hermes-weather-skill/1.0"
CREDIT = "Weather data by Open-Meteo.com (CC BY 4.0, https://open-meteo.com/); location data based on GeoNames."

UNITS = {  # request parameters, then the labels printed with the numbers
    "imperial": ({"temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "precipitation_unit": "inch"},
                 ("°F", "mph", "in")),
    "metric": ({}, ("°C", "km/h", "mm")),
}

# WMO weather codes, as listed at https://open-meteo.com/en/docs
WMO = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall", 77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 97: "Heavy thunderstorm",
    99: "Thunderstorm with heavy hail",
}


def get_json(url, params):
    request = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def geocode(name):
    """The best match for a place name; a state or country after a comma narrows it ("Paris, France")."""
    results = get_json(GEOCODE_URL, {"name": name, "count": 1, "language": "en", "format": "json"}).get("results")
    if not results:
        sys.exit(f"No place found for '{name}'. Add a state or country, for example 'Springfield, IL'.")
    place = results[0]
    label = ", ".join(part for part in (place.get("name"), place.get("admin1"), place.get("country")) if part)
    return place["latitude"], place["longitude"], label


def describe(code):
    return WMO.get(code, f"Weather code {code}")


def main():
    parser = argparse.ArgumentParser(description="Current weather and a daily forecast from Open-Meteo.")
    parser.add_argument("place", nargs="?", help='place name, e.g. "Los Angeles, CA"')
    parser.add_argument("--lat", type=float, help="latitude, instead of a place name")
    parser.add_argument("--lon", type=float, help="longitude, instead of a place name")
    parser.add_argument("--days", type=int, default=3, choices=range(1, 17), metavar="1-16",
                        help="forecast days (default 3)")
    parser.add_argument("--units", choices=UNITS, default="metric", help="imperial (°F, mph, in) or metric (default)")
    args = parser.parse_args()

    try:
        if args.lat is not None and args.lon is not None:
            lat, lon, label = args.lat, args.lon, None
        elif args.place:
            lat, lon, label = geocode(args.place)
        else:
            parser.error("give a place name, or both --lat and --lon")

        unit_params, (deg, wind, rain) = UNITS[args.units]
        data = get_json(FORECAST_URL, {
            "latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": args.days,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,"
                     "precipitation_sum,wind_speed_10m_max",
            **unit_params,
        })
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        sys.exit(f"Open-Meteo request failed: {exc}")

    now, day = data["current"], data["daily"]
    where = f"{label} ({lat:.2f}, {lon:.2f})" if label else f"{lat:.2f}, {lon:.2f}"
    print(f"{where}, time zone {data.get('timezone', 'unknown')}")
    clock = datetime.fromisoformat(now["time"]).strftime("%I:%M %p").lstrip("0")
    print(f"Now ({clock}): {now['temperature_2m']:.0f}{deg}, {describe(now['weather_code'])}, "
          f"wind {now['wind_speed_10m']:.0f} {wind}")
    for i, iso in enumerate(day["time"]):
        d = date.fromisoformat(iso)
        chance = day["precipitation_probability_max"][i]
        print(f"{d:%a}, {d:%b} {d.day}: {describe(day['weather_code'][i])}, "
              f"high {day['temperature_2m_max'][i]:.0f}{deg}, low {day['temperature_2m_min'][i]:.0f}{deg}, "
              f"rain chance {'n/a' if chance is None else f'{chance}%'} ({day['precipitation_sum'][i]:.2f} {rain}), "
              f"wind up to {day['wind_speed_10m_max'][i]:.0f} {wind}")
    print(CREDIT)


if __name__ == "__main__":
    main()
