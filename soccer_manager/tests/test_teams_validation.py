"""Tests for teams data validation."""

import pytest

from data_loader import load_teams


class TestTeamsValidation:
    """Tests to validate teams data is well-formed."""

    def test_all_teams_have_league(self):
        """Test that all teams have a league field."""
        teams = load_teams()
        for name, info in teams.items():
            assert "league" in info, f"Team '{name}' should have 'league' field"

    def test_all_teams_have_group(self):
        """Test that all teams have a group field."""
        teams = load_teams()
        for name, info in teams.items():
            assert "group" in info, f"Team '{name}' should have 'group' field"

    def test_all_teams_have_wiki(self):
        """Test that all teams have a wiki field."""
        teams = load_teams()
        for name, info in teams.items():
            assert "wiki" in info, f"Team '{name}' should have 'wiki' field"

    def test_league_values_are_valid(self):
        """Test that all league values are valid."""
        teams = load_teams()
        valid_leagues = {"First Division", "Ascenso"}
        for name, info in teams.items():
            assert info["league"] in valid_leagues, \
                f"Team '{name}' has invalid league '{info['league']}'"

    def test_first_division_groups_are_none(self):
        """Test that First Division teams have None as group."""
        teams = load_teams()
        for name, info in teams.items():
            if info["league"] == "First Division":
                assert info["group"] is None, \
                    f"First Division team '{name}' should have group=None"

    def test_ascenso_teams_have_group(self):
        """Test that Ascenso teams have a group assigned."""
        teams = load_teams()
        for name, info in teams.items():
            if info["league"] == "Ascenso":
                assert info["group"] is not None, \
                    f"Ascenso team '{name}' should have a group assigned"

    def test_wiki_url_format(self):
        """Test that wiki URLs are valid if present."""
        teams = load_teams()
        for name, info in teams.items():
            if info["wiki"]:
                assert info["wiki"].startswith("http"), \
                    f"Team '{name}' has invalid wiki URL format"

    def test_no_duplicate_team_names(self):
        """Test that there are no duplicate team names."""
        teams = load_teams()
        names = list(teams.keys())
        assert len(names) == len(set(names)), "Duplicate team names found"
