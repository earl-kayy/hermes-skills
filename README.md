# hermes-skills

Skills for [Hermes Agent](https://github.com/NousResearch/hermes-agent), published as a Hermes skill tap: add this
repository as a tap, then install a skill by its path.

## open-meteo-weather

Current weather and a daily forecast for any place, from the free [Open-Meteo](https://open-meteo.com/) API. The script is
standard-library Python 3, so it needs no API key and nothing to install.

### Install

```bash
hermes skills tap add earl-kayy/hermes-skills
hermes skills install earl-kayy/hermes-skills/skills/open-meteo-weather --yes
```

`--yes` skips the confirmation prompt; leave it out to review Hermes' security scan before the skill is installed.

Hermes v0.22.6 lists an install by this identifier under the source label "skills.sh". That catalog source answers bare
`owner/repo/...` identifiers before the GitHub tap source does, but it downloads the files from this repository, and the
install prints the GitHub tree it used. The skill isn't listed on skills.sh itself.

### Use

Ask Hermes about the weather, or preload the skill for one question:

```bash
hermes chat -q "What's the weather in Seattle today? Use °F." -s open-meteo-weather
```

The skill has the agent run one command through Hermes' terminal tool:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/weather.py "Seattle, WA" --days 1 --units imperial
```

```
Seattle, Washington, United States (47.61, -122.33), time zone America/Los_Angeles
Now (11:30 PM): 49°F, Overcast, wind 7 mph
Thu, Nov 5: Overcast, high 57°F, low 47°F, rain chance 16% (0.00 in), wind up to 7 mph
Weather data by Open-Meteo.com (CC BY 4.0, https://open-meteo.com/); location data based on GeoNames.
```

That's a real run from 11:30 PM Pacific on Nov 5, 2026. A place can be a city name, optionally followed by a state or country ("Paris, France"),
or coordinates with `--lat` and `--lon`. `--days` takes 1 to 16, and `--units` takes `imperial` or `metric` (the default).

### Requirements

- Python 3.8 or later, standard library only.
- Outbound HTTPS to `geocoding-api.open-meteo.com` and `api.open-meteo.com`.
- Hermes' terminal tool, which is on by default. The skill declares Linux and macOS.

### Data and credit

- Weather data by Open-Meteo.com, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Place names come from
  GeoNames, through Open-Meteo's geocoding API.
- Open-Meteo's free API is for non-commercial use, up to 10,000 calls a day.
- The skill tells the agent to end every weather answer with "Weather data by Open-Meteo.com".

## License

MIT, see [LICENSE](LICENSE). The weather data carries its own license, CC BY 4.0.
