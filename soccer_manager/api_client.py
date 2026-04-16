"""API Client Module - Fetches data from TheSportsDB API."""

import json
from typing import Any
from urllib.request import urlopen
from urllib.error import URLError

API_KEY = "123"
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"
HONDURAS_LEAGUE = "Honduras_Liga_Nacional_de_Futbol"


def fetch_json(url: str) -> dict[str, Any] | None:
    """Fetch JSON data from a URL. Returns None on error."""
    try:
        with urlopen(url, timeout=10) as response:
            return json.load(response)
    except (URLError, json.JSONDecodeError, TimeoutError):
        return None


def fetch_honduras_teams() -> list[dict[str, Any]]:
    """Fetch all teams from Honduras Liga Nacional."""
    url = f"{BASE_URL}/search_all_teams.php?l={HONDURAS_LEAGUE}"
    data = fetch_json(url)
    if data and data.get("teams"):
        return data["teams"]
    return []


def fetch_team_by_name(name: str) -> dict[str, Any] | None:
    """Fetch a specific team by name."""
    url = f"{BASE_URL}/searchteams.php?t={name.replace(' ', '_')}"
    data = fetch_json(url)
    if data and data.get("teams") and len(data["teams"]) > 0:
        return data["teams"][0]
    return None


def fetch_league_next_events(league_id: str = "4818", limit: int = 10) -> list[dict[str, Any]]:
    """Fetch upcoming events for a league."""
    url = f"{BASE_URL}/eventsnextleague.php?id={league_id}"
    data = fetch_json(url)
    if data and data.get("events"):
        return data["events"][:limit]
    return []


def fetch_league_past_events(league_id: str = "4818", limit: int = 10) -> list[dict[str, Any]]:
    """Fetch past events for a league."""
    url = f"{BASE_URL}/eventspastleague.php?id={league_id}"
    data = fetch_json(url)
    if data and data.get("events"):
        return data["events"][:limit]
    return []


def convert_api_team_to_local(api_team: dict[str, Any]) -> dict[str, Any]:
    """Convert API team format to local format."""
    return {
        "name": api_team.get("strTeam", ""),
        "league": "First Division",
        "group": None,
        "wiki": f"https://en.wikipedia.org/wiki/{api_team.get('strTeam', '').replace(' ', '_')}",
        "badge": api_team.get("strBadge"),
        "stadium": api_team.get("strStadium"),
        "capacity": api_team.get("intStadiumCapacity"),
        "founded": api_team.get("intFormedYear"),
        "location": api_team.get("strLocation"),
    }


def get_team_badge_url(team_name: str) -> str | None:
    """Get the badge URL for a team."""
    team = fetch_team_by_name(team_name)
    if team:
        return team.get("strBadge")
    return None


def is_api_available() -> bool:
    """Check if TheSportsDB API is available."""
    data = fetch_honduras_teams()
    return len(data) > 0