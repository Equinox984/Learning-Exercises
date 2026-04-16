"""Tests for trivia validation."""

import pytest
import random

from data_loader import load_trivia


class TestTriviaValidation:
    """Tests to validate trivia questions are well-formed."""

    def test_all_questions_have_text(self):
        """Test that all questions have non-empty question text."""
        trivia = load_trivia()
        for q in trivia:
            assert q["question"], "Question text should not be empty"
            assert len(q["question"]) > 5, "Question text should be descriptive"

    def test_all_options_are_unique(self):
        """Test that all options for each question are unique."""
        trivia = load_trivia()
        for q in trivia:
            assert len(q["options"]) == len(set(q["options"])), \
                f"Options for '{q['question'][:30]}...' should be unique"

    def test_answer_matches_option(self):
        """Test that answer exactly matches one of the options."""
        trivia = load_trivia()
        for q in trivia:
            assert q["answer"] in q["options"], \
                f"Answer '{q['answer']}' must be in options for '{q['question'][:30]}...'"

    def test_options_are_strings(self):
        """Test that all options are strings."""
        trivia = load_trivia()
        for q in trivia:
            for opt in q["options"]:
                assert isinstance(opt, str), "All options should be strings"

    def test_answer_is_string(self):
        """Test that answer is a string."""
        trivia = load_trivia()
        for q in trivia:
            assert isinstance(q["answer"], str), "Answer should be a string"

    def test_trivia_sampling_works(self):
        """Test that random.sample works with trivia questions."""
        trivia = load_trivia()
        sample = random.sample(trivia, min(5, len(trivia)))
        assert len(sample) == min(5, len(trivia))
        assert all(q in trivia for q in sample)
