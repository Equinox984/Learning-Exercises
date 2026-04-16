"""Score Manager Module - Handles score persistence."""

import json
from pathlib import Path

from data_loader import get_data_path, load_scores


def save_scores(highest_score: int | None, total_games: int) -> None:
    """Save scores to JSON file."""
    filepath = get_data_path() / "scores.json"
    data = {
        "highest_score": highest_score,
        "total_games_played": total_games,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_highest_score() -> int | None:
    """Get the highest score from persistence."""
    scores = load_scores()
    return scores.get("highest_score")


def get_total_games() -> int:
    """Get the total number of games played."""
    scores = load_scores()
    return scores.get("total_games_played", 0)


def update_highest_score(new_score: int) -> int | None:
    """Update highest score if new score is higher. Returns new highest."""
    current_highest = get_highest_score()
    if current_highest is None or new_score > current_highest:
        save_scores(new_score, get_total_games() + 1)
        return new_score
    else:
        save_scores(current_highest, get_total_games() + 1)
        return current_highest
