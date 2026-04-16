"""Data Loader Module - Loads data from JSON files with optional API enhancement."""

import json
from pathlib import Path
from typing import Any

import api_client


def get_data_path() -> Path:
    """Returns the path to the data directory."""
    return Path(__file__).parent / "data"


def load_json(filename: str) -> dict[str, Any]:
    """Load and return data from a JSON file."""
    filepath = get_data_path() / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_teams() -> dict[str, dict[str, Any]]:
    """Load teams data from JSON, enhanced with API data if available."""
    local_data = load_json("teams.json")
    teams = local_data["teams"]

    if api_client.is_api_available():
        api_teams = api_client.fetch_honduras_teams()
        if api_teams:
            for api_team in api_teams:
                api_converted = api_client.convert_api_team_to_local(api_team)
                team_name = api_converted["name"]
                if team_name in teams:
                    if api_converted.get("badge"):
                        teams[team_name]["badge"] = api_converted["badge"]
                    if api_converted.get("stadium"):
                        teams[team_name]["stadium"] = api_converted["stadium"]
                    if api_converted.get("capacity"):
                        teams[team_name]["capacity"] = api_converted["capacity"]
                    if api_converted.get("founded"):
                        teams[team_name]["founded"] = api_converted["founded"]
                    if api_converted.get("location"):
                        teams[team_name]["location"] = api_converted["location"]

    return teams


def load_matches() -> dict[str, list[dict[str, str]]]:
    """Load matches data from JSON, updated with API data if available."""
    local_matches = load_json("matches.json")

    if api_client.is_api_available():
        api_events = api_client.fetch_league_next_events()
        if api_events:
            first_div = []
            second_div = []
            for event in api_events:
                hometeam = event.get("strHomeTeam", "")
                awayteam = event.get("strAwayTeam", "")
                date = event.get("strDate", "")
                if hometeam and awayteam and date:
                    match = {
                        "home": hometeam,
                        "away": awayteam,
                        "stadium": event.get("strStadium", ""),
                        "date": date,
                    }
                    if event.get("idLeague") == "4818":
                        first_div.append(match)
                    else:
                        second_div.append(match)

            first_div = first_div[:3] if first_div else local_matches.get("first_division", [])
            second_div = second_div[:3] if second_div else local_matches.get("second_division", [])

            if first_div or second_div:
                local_matches = {
                    "first_division": first_div or local_matches.get("first_division", []),
                    "second_division": second_div or local_matches.get("second_division", []),
                }

    return local_matches


def load_trivia() -> list[dict[str, Any]]:
    """Load trivia questions from JSON."""
    data = load_json("trivia.json")
    return data["trivia"]


def load_scores() -> dict[str, int | None]:
    """Load scores data from JSON."""
    return load_json("scores.json")
