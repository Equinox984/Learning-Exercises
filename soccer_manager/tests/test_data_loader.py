"""Tests for data_loader module."""

import pytest
from data_loader import (
    get_data_path,
    load_teams,
    load_matches,
    load_trivia,
    load_scores,
)


class TestDataPath:
    """Tests for get_data_path function."""

    def test_get_data_path_returns_path(self):
        """Test that get_data_path returns a valid path."""
        result = get_data_path()
        assert result is not None
        assert str(result).endswith("data")

    def test_get_data_path_exists(self):
        """Test that data path exists."""
        result = get_data_path()
        assert result.exists()


class TestLoadTeams:
    """Tests for load_teams function."""

    def test_load_teams_returns_dict(self):
        """Test that load_teams returns a dictionary."""
        result = load_teams()
        assert isinstance(result, dict)

    def test_load_teams_not_empty(self):
        """Test that teams data is not empty."""
        result = load_teams()
        assert len(result) > 0

    def test_load_teams_has_first_division(self):
        """Test that there are First Division teams."""
        teams = load_teams()
        first_div = [t for t, info in teams.items() if info["league"] == "First Division"]
        assert len(first_div) > 0

    def test_load_teams_has_ascenso(self):
        """Test that there are Ascenso teams."""
        teams = load_teams()
        ascenso = [t for t, info in teams.items() if info["league"] == "Ascenso"]
        assert len(ascenso) > 0

    def test_team_has_required_fields(self):
        """Test that each team has required fields."""
        teams = load_teams()
        for name, info in teams.items():
            assert "league" in info
            assert "group" in info
            assert "wiki" in info

    def test_olimpia_is_first_division(self):
        """Test that Olimpia is correctly marked as First Division."""
        teams = load_teams()
        assert "Olimpia" in teams
        assert teams["Olimpia"]["league"] == "First Division"

    def test_teams_with_wiki_have_url(self):
        """Test that teams with wiki have valid URLs."""
        teams = load_teams()
        for name, info in teams.items():
            if info["wiki"]:
                assert info["wiki"].startswith("http")


class TestLoadMatches:
    """Tests for load_matches function."""

    def test_load_matches_returns_dict(self):
        """Test that load_matches returns a dictionary."""
        result = load_matches()
        assert isinstance(result, dict)

    def test_load_matches_has_first_division(self):
        """Test that matches has first division matches."""
        matches = load_matches()
        assert "first_division" in matches
        assert isinstance(matches["first_division"], list)

    def test_load_matches_has_second_division(self):
        """Test that matches has second division matches."""
        matches = load_matches()
        assert "second_division" in matches
        assert isinstance(matches["second_division"], list)

    def test_match_has_required_fields(self):
        """Test that each match has required fields."""
        matches = load_matches()
        for match in matches["first_division"]:
            assert "home" in match
            assert "away" in match
            assert "stadium" in match
            assert "date" in match


class TestLoadTrivia:
    """Tests for load_trivia function."""

    def test_load_trivia_returns_list(self):
        """Test that load_trivia returns a list."""
        result = load_trivia()
        assert isinstance(result, list)

    def test_load_trivia_has_multiple_questions(self):
        """Test that there are at least 5 trivia questions."""
        result = load_trivia()
        assert len(result) >= 5

    def test_trivia_question_has_required_fields(self):
        """Test that each trivia question has required fields."""
        trivia = load_trivia()
        for question in trivia:
            assert "question" in question
            assert "options" in question
            assert "answer" in question

    def test_trivia_has_four_options(self):
        """Test that each trivia question has exactly 4 options."""
        trivia = load_trivia()
        for question in trivia:
            assert len(question["options"]) == 4

    def test_trivia_answer_in_options(self):
        """Test that the answer is one of the options."""
        trivia = load_trivia()
        for question in trivia:
            assert question["answer"] in question["options"]


class TestLoadScores:
    """Tests for load_scores function."""

    def test_load_scores_returns_dict(self):
        """Test that load_scores returns a dictionary."""
        result = load_scores()
        assert isinstance(result, dict)

    def test_load_scores_has_highest_score(self):
        """Test that scores has highest_score field."""
        scores = load_scores()
        assert "highest_score" in scores

    def test_load_scores_has_total_games(self):
        """Test that scores has total_games_played field."""
        scores = load_scores()
        assert "total_games_played" in scores
