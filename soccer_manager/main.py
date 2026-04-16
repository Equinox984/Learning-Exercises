"""Soccer Manager Engine - Refactored with type hints and JSON persistence."""

import random
import os
import sys
import unicodedata
from typing import Callable

from data_loader import load_teams, load_matches, load_trivia
from score_manager import get_highest_score, update_highest_score


TEAMS = load_teams()
FIRST_DIVISION_MATCHES = load_matches()["first_division"]
SECOND_DIVISION_MATCHES = load_matches()["second_division"]
TRIVIA_QUESTIONS = load_trivia()

SEPARATOR = "=" * 50
MINI_SEPARATOR = "-" * 30
TRIVIA_QUESTION_COUNT = 5

PROMPT_CHOICE = "(Press a number to continue)"
PROMPT_ENTER = "Press Enter to continue..."
ERROR_INVALID = "Invalid choice. Please select {}."


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def normalize_text(text: str) -> str:
    """Remove accents and convert to lowercase for search comparisons."""
    normalized = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def show_menu(title: str, options: list[tuple[str, str]], exit_num: str) -> str:
    """
    Display a menu and return the user's choice.
    
    Args:
        title: Menu title to display.
        options: List of (option_number, option_description) tuples.
        exit_num: Number that triggers exit.
    
    Returns:
        The chosen option number or exit_num to handle exit.
    """
    menu_text = f"""
{title}

"""
    for num, desc in options:
        menu_text += f"[{num}] {desc}\n"
    menu_text += f"\n{PROMPT_CHOICE}\n\n-> "
    
    return input(menu_text).strip()


def run_menu(
    title: str,
    options: list[tuple[str, str]],
    actions: dict[str, Callable[[], None]],
) -> None:
    """
    Run a menu loop handling user choices.
    
    Args:
        title: Menu title.
        options: List of (option_number, option_description) tuples.
        actions: Dict mapping choice strings to their handler functions.
    """
    clear_screen()
    while True:
        choice = show_menu(title, options, "exit")
        
        if choice in actions:
            actions[choice]()
        elif choice == "exit":
            clear_screen()
            break
        else:
            clear_screen()
            valid = ", ".join(actions.keys())
            print(f"\nERROR: {ERROR_INVALID.format(valid)}\n")


def get_first_division_teams() -> list[str]:
    """Returns a sorted list of first division team names."""
    return sorted(
        name for name, info in TEAMS.items() if info["league"] == "First Division"
    )


def get_ascenso_by_groups() -> dict[str, list[str]]:
    """Returns teams grouped by their Ascenso division groups."""
    groups: dict[str, list[str]] = {}
    for name, info in TEAMS.items():
        if info["league"] == "Ascenso":
            group_name = info["group"]
            if group_name and group_name not in groups:
                groups[group_name] = []
            if group_name:
                groups[group_name].append(name)
    for group_name in groups:
        groups[group_name] = sorted(groups[group_name])
    return groups


def display_leagues() -> None:
    """Display all Honduran leagues and their teams."""
    clear_screen()
    while True:
        choice = input(
            """
--- Honduran Leagues ---
[1] Honduran National Professional Football League (First Division)
[2] Honduran Second Division (Ascenso League)
[3] Exit

"""

            + PROMPT_CHOICE + "\n\n-> "
        ).strip()

        if choice == "1":
            clear_screen()
            teams = get_first_division_teams()
            print(f"\n{SEPARATOR}\n  First Division Teams\n{SEPARATOR}")
            for number, team in enumerate(teams, 1):
                print(f"  {number}. {team}")
            print(f"{SEPARATOR}\n")
            input(PROMPT_ENTER)
            clear_screen()

        elif choice == "2":
            clear_screen()
            groups = get_ascenso_by_groups()
            print(f"\n{SEPARATOR}\n  Second Division (Ascenso League)\n{SEPARATOR}")
            for group_name, teams in sorted(groups.items()):
                print(f"\n   {group_name}\n {MINI_SEPARATOR}")
                for number, team in enumerate(teams, 1):
                    print(f"    {number}. {team}")
            print(f"\n{SEPARATOR}\n")
            input(PROMPT_ENTER)
            clear_screen()

        elif choice == "3":
            clear_screen()
            break
        else:
            clear_screen()
            print(f"\nERROR: {ERROR_INVALID.format('1, 2, or 3')}\n")


def finder() -> None:
    """Team finder - search for teams and display their info."""
    clear_screen()
    print(
        """
--- Finder ---
Search for a team to get its information.
"""
    )
    while True:
        query = input("Write the team name (or 'exit' to go back) -> ").strip()
        if query.lower() == "exit":
            clear_screen()
            break

        if not query:
            print("\nERROR: Please enter a valid team name.\n")
            continue

        query_normalized = normalize_text(query)

        matches = [
            name for name in TEAMS
            if normalize_text(name) == query_normalized
        ]

        if not matches:
            partial_matches = [
                name for name in TEAMS
                if normalize_text(name).startswith(query_normalized)
            ]

            if partial_matches:
                clear_screen()
                print("\nDid you mean?\n")
                for team in sorted(partial_matches):
                    print(f"  - {team}")
                print()
            else:
                clear_screen()
                print(f"\nERROR: '{query}' not found in the database.\n")
        else:
            match_name = matches[0]
            clear_screen()
            team_data = TEAMS[match_name]
            wiki_url = team_data["wiki"]
            group_info = team_data["group"] or "N/A"

            print(f"\n{SEPARATOR}")
            print(f"\nTeam: {match_name}")
            print(f"League: {team_data['league']}")
            print(f"Group: {group_info}")
            if wiki_url:
                print(f"Wikipedia: {wiki_url}")
            else:
                print("Wikipedia: No Wikipedia URL found for this team.")
            print(f"\n{SEPARATOR}\n")


def soccer_information() -> None:
    """Soccer information menu."""
    clear_screen()
    while True:
        choice = input(
            """
=== Soccer General Info Menu ===

[1] Honduran Leagues & Teams
[2] Finder
[3] Exit

"""

            + PROMPT_CHOICE + "\n\n-> "
        ).strip()

        if choice == "1":
            display_leagues()
        elif choice == "2":
            finder()
        elif choice == "3":
            clear_screen()
            break
        else:
            clear_screen()
            print(f"\nERROR: {ERROR_INVALID.format('1, 2, or 3')}\n")


def display_matches(matches: list[dict[str, str]], title: str) -> None:
    """Display a list of matches."""
    clear_screen()
    print(f"\n{SEPARATOR}")
    print(f"\nUPCOMING MATCHES - {title}\n\n{SEPARATOR}\n")

    for match in matches:
        print(MINI_SEPARATOR)
        print(f" {match['home']} vs {match['away']}")
        print(f"    Stadium: {match['stadium']} | Date: {match['date']}")
        print(MINI_SEPARATOR)

    input("\nPress Enter to go back -> ")
    clear_screen()


def matches_menu() -> None:
    """Matches menu."""
    clear_screen()
    while True:
        choice = input(
            """
=== Matches Menu ===

[1] First Division Matches
[2] Second Division Matches
[3] Exit

"""

            + PROMPT_CHOICE + "\n\n-> "
        ).strip()

        if choice == "1":
            display_matches(FIRST_DIVISION_MATCHES, "First Division")
        elif choice == "2":
            display_matches(SECOND_DIVISION_MATCHES, "Second Division")
        elif choice == "3":
            clear_screen()
            break
        else:
            clear_screen()
            print(f"\nERROR: {ERROR_INVALID.format('1, 2, or 3')}\n")


def play_trivia() -> int:
    """Play a round of trivia. Returns the score achieved."""
    clear_screen()
    print("--- Trivia Minigame ---\n")

    sample_size = min(TRIVIA_QUESTION_COUNT, len(TRIVIA_QUESTIONS))
    questions = random.sample(TRIVIA_QUESTIONS, sample_size)
    score = 0

    for question_number, question in enumerate(questions, 1):
        print(f"Q{question_number}: {question['question']}\n")
        for option_number, option in enumerate(question["options"], 1):
            print(f"  [{option_number}] {option}")

        answer_input = input("\nAnswer: ").strip()
        num_options = len(question["options"])

        try:
            answer_idx = int(answer_input) - 1
            if 0 <= answer_idx < num_options:
                selected = question["options"][answer_idx]
                if selected == question["answer"]:
                    print("Correct!\n")
                    score += 1
                else:
                    print(f"Incorrect. The answer was: {question['answer']}\n")
            else:
                print(f"Invalid option. The answer was: {question['answer']}\n")
        except ValueError:
            print(f"Invalid input. The answer was: {question['answer']}\n")

    return score


def show_highest_score() -> None:
    """Display the highest score."""
    clear_screen()
    highest = get_highest_score()

    if highest is None:
        print("\nNo games played yet.\n")
    else:
        print(f"\n{SEPARATOR}")
        print(f"  Highest Score: {highest}/{TRIVIA_QUESTION_COUNT}")
        print(f"{SEPARATOR}\n")

    input(PROMPT_ENTER + " -> ")
    clear_screen()


def trivia_minigame() -> None:
    """Trivia minigame menu."""
    clear_screen()
    while True:
        choice = input(
            """
=== Trivia Menu ===

[1] Start Trivia Minigame
[2] Last Highest Score
[3] Exit

"""

            + PROMPT_CHOICE + "\n\n-> "
        ).strip()

        if choice == "1":
            score = play_trivia()
            new_highest = update_highest_score(score)

            print(f"{SEPARATOR}")
            print(f"  Final score: {score}/{TRIVIA_QUESTION_COUNT}")
            if new_highest == score and score > 0:
                print("  NEW HIGH SCORE!")
            print(f"{SEPARATOR}\n")
            input(PROMPT_ENTER + " -> ")
            clear_screen()

        elif choice == "2":
            show_highest_score()

        elif choice == "3":
            clear_screen()
            break
        else:
            clear_screen()
            print(f"\nERROR: {ERROR_INVALID.format('1, 2, or 3')}\n")


def main() -> None:
    """Main entry point."""
    clear_screen()
    while True:
        choice = input(
            """
===== Welcome to the Soccer Manager =====

[1] Soccer Information
[2] Matches
[3] Trivia Minigame
[4] Exit

"""

            + PROMPT_CHOICE + "\n\n-> "
        ).strip()

        if choice == "1":
            soccer_information()
        elif choice == "2":
            matches_menu()
        elif choice == "3":
            trivia_minigame()
        elif choice == "4":
            clear_screen()
            print("\nThanks for using Soccer Manager! Goodbye!\n")
            sys.exit(0)
        else:
            clear_screen()
            print(f"\nERROR: {ERROR_INVALID.format('1, 2, 3, or 4')}\n")


if __name__ == "__main__":
    main()
