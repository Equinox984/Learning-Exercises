"""Tests for main module functions."""

import pytest
from unittest.mock import patch, MagicMock

from main import (
    get_first_division_teams,
    get_ascenso_by_groups,
)


class TestGetFirstDivisionTeams:
    """Tests for get_first_division_teams function."""

    def test_returns_list(self):
        """Test that function returns a list."""
        result = get_first_division_teams()
        assert isinstance(result, list)

    def test_returns_sorted(self):
        """Test that returned list is sorted alphabetically."""
        result = get_first_division_teams()
        assert result == sorted(result)

    def test_contains_expected_teams(self):
        """Test that expected teams are present."""
        result = get_first_division_teams()
        expected = ["Olimpia", "Motagua", "Real España"]
        for team in expected:
            assert team in result

    def test_excludes_ascenso_teams(self):
        """Test that Ascenso teams are not in the result."""
        result = get_first_division_teams()
        ascenso_team = "Boca Juniors"
        assert ascenso_team not in result


class TestGetAscensoByGroups:
    """Tests for get_ascenso_by_groups function."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = get_ascenso_by_groups()
        assert isinstance(result, dict)

    def test_groups_are_sorted(self):
        """Test that all groups in result are sorted."""
        result = get_ascenso_by_groups()
        for group_name, teams in result.items():
            assert teams == sorted(teams)

    def test_has_group_a(self):
        """Test that Group A exists."""
        result = get_ascenso_by_groups()
        assert "Group A" in result

    def test_group_a_contains_vida(self):
        """Test that Vida is in Group A."""
        result = get_ascenso_by_groups()
        assert "Vida" in result.get("Group A", [])

    def test_all_groups_sorted_alphabetically(self):
        """Test that groups are sorted alphabetically by name."""
        result = get_ascenso_by_groups()
        group_names = list(result.keys())
        assert group_names == sorted(group_names)

    def test_no_duplicate_teams_in_groups(self):
        """Test that no team appears in multiple groups."""
        result = get_ascenso_by_groups()
        all_teams = []
        for teams in result.values():
            all_teams.extend(teams)
        assert len(all_teams) == len(set(all_teams))
