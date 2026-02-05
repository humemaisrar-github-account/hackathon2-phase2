"""
Unit tests for CLI input validation and handling.
"""
import pytest
from unittest.mock import patch
from src.lib.utils import (
    validate_menu_option,
    validate_task_id,
    validate_non_empty_input,
    validate_string_length,
    get_user_input
)


def test_validate_menu_option_valid():
    """Test validation of valid menu options."""
    assert validate_menu_option("1", [1, 2, 3, 4, 5, 6]) == True
    assert validate_menu_option("6", [1, 2, 3, 4, 5, 6]) == True


def test_validate_menu_option_invalid():
    """Test validation of invalid menu options."""
    assert validate_menu_option("7", [1, 2, 3, 4, 5, 6]) == False
    assert validate_menu_option("a", [1, 2, 3, 4, 5, 6]) == False
    assert validate_menu_option("", [1, 2, 3, 4, 5, 6]) == False


def test_validate_task_id_valid():
    """Test validation of valid task IDs."""
    assert validate_task_id("1") == True
    assert validate_task_id("10") == True


def test_validate_task_id_invalid():
    """Test validation of invalid task IDs."""
    assert validate_task_id("0") == False
    assert validate_task_id("-1") == False
    assert validate_task_id("a") == False
    assert validate_task_id("") == False


def test_validate_task_id_with_max():
    """Test validation of task IDs with max constraint."""
    assert validate_task_id("3", max_id=5) == True
    assert validate_task_id("6", max_id=5) == False


def test_validate_non_empty_input():
    """Test validation of non-empty input."""
    assert validate_non_empty_input("valid input") == True
    assert validate_non_empty_input("   input   ") == True  # with whitespace around
    assert validate_non_empty_input("") == False
    assert validate_non_empty_input("   ") == False  # only whitespace


def test_validate_string_length_valid():
    """Test validation of string length within limits."""
    assert validate_string_length("short", max_length=10) == True
    assert validate_string_length("exact length", max_length=12) == True


def test_validate_string_length_invalid():
    """Test validation of string length exceeding limits."""
    assert validate_string_length("this is too long", max_length=5) == False


@patch('builtins.input', return_value='test input')
def test_get_user_input(mock_input):
    """Test getting user input with stripping."""
    result = get_user_input("Enter something: ")
    assert result == "test input"