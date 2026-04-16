"""Simple validation script to verify the refactored code works correctly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data_loader import load_teams, load_matches, load_trivia, load_scores
from score_manager import get_highest_score, update_highest_score, get_total_games
from main import get_first_division_teams, get_ascenso_by_groups


def test_data_loading():
    """Test data loading functions."""
    print("Testing data loading...")

    teams = load_teams()
    assert len(teams) > 0, "Teams should not be empty"
    print(f"  - Loaded {len(teams)} teams")

    matches = load_matches()
    assert "first_division" in matches
    assert "second_division" in matches
    print(f"  - Loaded matches data")

    trivia = load_trivia()
    assert len(trivia) >= 5, "Should have at least 5 trivia questions"
    print(f"  - Loaded {len(trivia)} trivia questions")

    scores = load_scores()
    assert "highest_score" in scores
    assert "total_games_played" in scores
    print(f"  - Loaded scores data")


def test_team_functions():
    """Test team-related functions."""
    print("\nTesting team functions...")

    first_div = get_first_division_teams()
    assert len(first_div) > 0, "Should have first division teams"
    assert first_div == sorted(first_div), "Should be sorted"
    print(f"  - First division teams: {len(first_div)}")

    ascenso = get_ascenso_by_groups()
    assert len(ascenso) > 0, "Should have ascenso groups"
    print(f"  - Ascenso groups: {len(ascenso)}")


def test_trivia_validation():
    """Test trivia question validation."""
    print("\nTesting trivia validation...")

    trivia = load_trivia()
    for q in trivia:
        assert q["question"], "Question text should not be empty"
        assert len(q["options"]) == 4, "Should have 4 options"
        assert q["answer"] in q["options"], "Answer should be in options"

    print(f"  - All {len(trivia)} trivia questions validated")


def test_score_persistence():
    """Test score persistence functions."""
    print("\nTesting score persistence...")

    initial_highest = get_highest_score()
    initial_games = get_total_games()

    new_score = 3
    new_highest = update_highest_score(new_score)
    assert new_highest >= new_score, "Highest should be updated"

    print(f"  - Score persistence working")


def test_wiki_handling():
    """Test wiki URL handling for teams without Wikipedia."""
    print("\nTesting wiki handling...")

    teams = load_teams()
    teams_without_wiki = [name for name, info in teams.items() if not info["wiki"]]
    teams_with_wiki = [name for name, info in teams.items() if info["wiki"]]

    print(f"  - Teams with Wikipedia: {len(teams_with_wiki)}")
    print(f"  - Teams without Wikipedia: {len(teams_without_wiki)}")

    for name in teams_without_wiki:
        assert teams[name]["wiki"] is None, f"Wiki should be None, not empty string"


def main():
    """Run all validation tests."""
    print("=" * 50)
    print("Soccer Manager Validation Tests")
    print("=" * 50)

    try:
        test_data_loading()
        test_team_functions()
        test_trivia_validation()
        test_score_persistence()
        test_wiki_handling()

        print("\n" + "=" * 50)
        print("All tests passed!")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
