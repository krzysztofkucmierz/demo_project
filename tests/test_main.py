"""Test the main module."""

from typing import Any

# import pytest
from app.main import main


def test_main(capsys: Any) -> None:
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "Demo Project is running!" in captured.out
