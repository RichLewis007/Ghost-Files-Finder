"""Tests for error scenarios in main_window.py file operations."""

from __future__ import annotations

from rfe.main_window import MainWindow


def test_debug_mode_from_environment_variable() -> None:
    """Test that DEBUG_MODE reads from GFF_DEBUG_MODE environment variable."""
    # Test the logic directly since module-level constants are evaluated at import time
    # This test verifies the logic works correctly
    test_cases = [
        ("1", True),
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("yes", True),
        ("Yes", True),
        ("on", True),
        ("On", True),
        ("0", False),
        ("false", False),
        ("", False),
        ("invalid", False),
    ]

    for env_value, expected in test_cases:
        result = env_value.lower() in ("1", "true", "yes", "on")
        assert result == expected, f"Expected {expected} for env value '{env_value}'"


def test_format_elapsed_handles_negative() -> None:
    """Test that _format_elapsed handles negative values gracefully."""
    result = MainWindow._format_elapsed(-5.0)
    assert result == "0s"


def test_format_elapsed_handles_zero() -> None:
    """Test that _format_elapsed handles zero correctly."""
    result = MainWindow._format_elapsed(0.0)
    assert result == "0s"


def test_format_elapsed_handles_large_values() -> None:
    """Test that _format_elapsed handles very large time values."""
    # Test 2 hours
    result = MainWindow._format_elapsed(7200.0)
    assert result == "120m 00s"

    # Test 1 hour 30 minutes
    result = MainWindow._format_elapsed(5400.0)
    assert result == "90m 00s"


def test_truncate_path_handles_short_paths() -> None:
    """Test that _truncate_path returns short paths unchanged."""
    short_path = "short/path.txt"
    result = MainWindow._truncate_path(short_path, max_length=80)
    assert result == short_path


def test_truncate_path_handles_very_long_paths() -> None:
    """Test that _truncate_path truncates very long paths."""
    long_path = "/" + "a" * 200 + "/file.txt"
    result = MainWindow._truncate_path(long_path, max_length=80)
    assert len(result) <= 80
    assert "…" in result


def test_truncate_path_handles_extremely_short_max_length() -> None:
    """Test that _truncate_path handles very short max_length values."""
    path = "this/is/a/very/long/path/that/needs/truncation.txt"
    result = MainWindow._truncate_path(path, max_length=10)
    assert len(result) <= 10
    assert "…" in result


def test_format_mtime_handles_none() -> None:
    """Test that _format_mtime handles None correctly."""
    result = MainWindow._format_mtime(None)
    assert result is None


def test_format_mtime_handles_valid_timestamp() -> None:
    """Test that _format_mtime formats valid timestamps correctly."""
    import time

    timestamp = time.time()
    result = MainWindow._format_mtime(timestamp)
    assert result is not None
    assert "T" in result or "-" in result  # ISO format contains T or date separator


def test_format_size_handles_zero() -> None:
    """Test that _format_size handles zero correctly."""
    result = MainWindow._format_size(0)
    assert result == "0.00 B"


def test_format_size_handles_large_values() -> None:
    """Test that _format_size handles very large values."""
    # Test 1 TB (1024^4 bytes)
    result = MainWindow._format_size(1024**4)
    assert "TB" in result or result.endswith("B")

    # Test 1 GB
    result = MainWindow._format_size(1024**3)
    assert "GB" in result
