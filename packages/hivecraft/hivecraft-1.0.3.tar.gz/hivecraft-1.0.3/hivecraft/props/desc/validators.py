from typing import Any

from hivecraft.ressources import PUZZLES_DIFFICULTY

def is_valid_difficulty(value: str) -> bool:
    """Checks if the difficulty is one of the predefined values."""
    return value in PUZZLES_DIFFICULTY

def is_valid_language_code(value: str) -> bool:
    """Checks if the string is a 2-letter language code (basic check)."""
    return isinstance(value, str) and len(value) == 2 and value.isalpha()

def is_non_empty_string(value: str) -> bool:
    """Checks if the value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())

def is_positive_or_zero_int(value: int) -> bool:
    """Checks if the value is an integer greater than or equal to 0."""
    return isinstance(value, int) and value >= 0