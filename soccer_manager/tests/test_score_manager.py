"""Tests for score_manager module."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from score_manager import (
    save_scores,
    get_highest_score,
    get_total_games,
    update_highest_score,
)


class TestSaveScores:
    """Tests for save_scores function."""

    def test_save_scores_creates_file(self, tmp_path):
        """Test that save_scores creates a JSON file."""
        with patch("score_manager.get_data_path", return_value=tmp_path):
            save_scores(5, 10)
            filepath = tmp_path / "scores.json"
            assert filepath.exists()

    def test_save_scores_writes_correct_data(self, tmp_path):
        """Test that save_scores writes correct data."""
        with patch("score_manager.get_data_path", return_value=tmp_path):
            save_scores(7, 15)
            filepath = tmp_path / "scores.json"
            with open(filepath) as f:
                data = json.load(f)
            assert data["highest_score"] == 7
            assert data["total_games_played"] == 15

    def test_save_scores_handles_none_highest(self, tmp_path):
        """Test that save_scores handles None for highest_score."""
        with patch("score_manager.get_data_path", return_value=tmp_path):
            save_scores(None, 0)
            filepath = tmp_path / "scores.json"
            with open(filepath) as f:
                data = json.load(f)
            assert data["highest_score"] is None


class TestGetHighestScore:
    """Tests for get_highest_score function."""

    def test_get_highest_score_returns_value(self):
        """Test that get_highest_score returns a value."""
        result = get_highest_score()
        assert result is None or isinstance(result, int)

    def test_get_highest_score_type(self):
        """Test that get_highest_score returns int or None."""
        result = get_highest_score()
        assert result is None or isinstance(result, int)


class TestGetTotalGames:
    """Tests for get_total_games function."""

    def test_get_total_games_returns_int(self):
        """Test that get_total_games returns an integer."""
        result = get_total_games()
        assert isinstance(result, int)
        assert result >= 0


class TestUpdateHighestScore:
    """Tests for update_highest_score function."""

    def test_update_highest_score_returns_int(self):
        """Test that update_highest_score returns an integer."""
        result = update_highest_score(3)
        assert isinstance(result, int)

    def test_update_highest_score_new_higher(self):
        """Test that higher score updates the highest."""
        initial = get_highest_score()
        new_score = 10 if (initial is None or initial < 10) else initial + 1
        result = update_highest_score(new_score)
        assert result >= new_score
