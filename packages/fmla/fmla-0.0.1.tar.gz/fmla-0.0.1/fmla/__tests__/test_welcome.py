"""Test welcome message functionality."""

from unittest.mock import patch

from fmla import welcome


def test_welcome_message() -> None:
    """Test that welcome message is printed."""
    with patch("builtins.print") as mock_print:
        welcome()
        mock_print.assert_called_once_with("Welcome to FMLA package!")


def test_welcome_function_exists() -> None:
    """Test that welcome function exists."""
    assert callable(welcome)
