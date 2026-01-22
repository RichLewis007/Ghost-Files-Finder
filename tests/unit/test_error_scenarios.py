"""Tests for error scenarios and edge cases."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from rfe.models.match_engine import MatchEngine
from rfe.models.rules_model import Rule, parse_filter_file


def test_parse_filter_file_nonexistent_path(tmp_path: Path) -> None:
    """Test that parsing a non-existent file raises ValueError."""
    nonexistent = tmp_path / "does_not_exist.txt"
    with pytest.raises(ValueError, match="Failed to read filter file"):
        parse_filter_file(nonexistent)


def test_parse_filter_file_permission_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that permission errors are caught and re-raised as ValueError."""
    filter_file = tmp_path / "filter.txt"
    filter_file.write_text("- **/*.tmp\n")

    def mock_read_text(*args: object, **kwargs: object) -> str:
        raise PermissionError("Permission denied")

    monkeypatch.setattr(Path, "read_text", mock_read_text)

    with pytest.raises(ValueError, match="Failed to read filter file"):
        parse_filter_file(filter_file)


def test_parse_filter_file_unicode_decode_error(tmp_path: Path) -> None:
    """Test that invalid UTF-8 files raise ValueError."""
    filter_file = tmp_path / "filter.txt"
    # Write binary data that's not valid UTF-8
    filter_file.write_bytes(b"\xff\xfe\x00\x01")

    with pytest.raises(ValueError, match="Failed to read filter file"):
        parse_filter_file(filter_file)


def test_match_engine_evaluate_path_outside_root(tmp_path: Path) -> None:
    """Test that evaluating a path outside the root raises ValueError."""
    root = tmp_path / "root"
    root.mkdir()
    outside_path = tmp_path / "outside" / "file.txt"
    outside_path.parent.mkdir()
    outside_path.write_text("test")

    rules = [Rule(action="-", pattern="**/*.txt", lineno=1)]
    engine = MatchEngine(rules)

    with pytest.raises(ValueError, match="is not in the subpath"):
        engine.evaluate_path(outside_path, root)


def test_match_engine_evaluate_path_symlink_loop(tmp_path: Path) -> None:
    """Test that symlink loops are handled gracefully."""
    if not hasattr(os, "symlink"):
        pytest.skip("Platform does not support symlinks")

    root = tmp_path / "root"
    root.mkdir()
    link_target = root / "target"
    link_target.mkdir()
    symlink = root / "link"
    symlink.symlink_to(link_target)

    rules = [Rule(action="-", pattern="**/link/**", lineno=1)]
    engine = MatchEngine(rules)

    # Should not raise an error, but may or may not match depending on os.walk behavior
    result = engine.evaluate_path(symlink, root)
    assert isinstance(result.decision.matched, bool)


def test_match_engine_empty_rules(tmp_path: Path) -> None:
    """Test that MatchEngine works with empty rules list."""
    engine = MatchEngine([])
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")

    result = engine.evaluate_path(test_file, tmp_path)
    assert result.decision.matched is False
    assert result.decision.rule_index is None
    assert result.decision.rule is None


def test_match_engine_path_with_special_characters(tmp_path: Path) -> None:
    """Test that paths with special characters are handled correctly."""
    rules = [Rule(action="-", pattern="**/*.txt", lineno=1)]
    engine = MatchEngine(rules)

    # Test with spaces
    file_with_spaces = tmp_path / "file with spaces.txt"
    file_with_spaces.write_text("test")
    result = engine.evaluate_path(file_with_spaces, tmp_path)
    assert result.decision.matched is True

    # Test with unicode characters
    file_unicode = tmp_path / "file_测试.txt"
    file_unicode.write_text("test")
    result = engine.evaluate_path(file_unicode, tmp_path)
    assert result.decision.matched is True


def test_parse_filter_file_empty_file(tmp_path: Path) -> None:
    """Test that parsing an empty file returns empty rules list."""
    filter_file = tmp_path / "empty.txt"
    filter_file.write_text("")

    rules = parse_filter_file(filter_file)
    assert rules == []


def test_parse_filter_file_only_comments(tmp_path: Path) -> None:
    """Test that parsing a file with only comments returns empty rules list."""
    filter_file = tmp_path / "comments.txt"
    filter_file.write_text("# This is a comment\n# Another comment\n  \n")

    rules = parse_filter_file(filter_file)
    assert rules == []


def test_parse_filter_file_only_include_rules(tmp_path: Path) -> None:
    """Test that parsing a file with only include rules returns empty list."""
    filter_file = tmp_path / "includes.txt"
    filter_file.write_text("+ **/*.txt\n+ **/*.md\n")

    rules = parse_filter_file(filter_file)
    assert rules == []


def test_match_engine_relative_to_nonexistent_root(tmp_path: Path) -> None:
    """Test that evaluating a path with non-existent root raises ValueError."""
    nonexistent_root = tmp_path / "nonexistent"
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")

    rules = [Rule(action="-", pattern="**/*.txt", lineno=1)]
    engine = MatchEngine(rules)

    with pytest.raises(ValueError, match="is not in the subpath"):
        engine.evaluate_path(test_file, nonexistent_root)


def test_match_engine_case_sensitive_mismatch(tmp_path: Path) -> None:
    """Test that case-sensitive matching works correctly."""
    rules = [Rule(action="-", pattern="**/Test.txt", lineno=1)]
    engine_sensitive = MatchEngine(rules, case_sensitive=True)
    engine_insensitive = MatchEngine(rules, case_sensitive=False)

    test_file = tmp_path / "test.txt"  # lowercase
    test_file.write_text("test")

    result_sensitive = engine_sensitive.evaluate_path(test_file, tmp_path)
    result_insensitive = engine_insensitive.evaluate_path(test_file, tmp_path)

    assert result_sensitive.decision.matched is False
    assert result_insensitive.decision.matched is True


def test_parse_filter_file_invalid_metadata_format(tmp_path: Path) -> None:
    """Test that invalid metadata comments are ignored."""
    filter_file = tmp_path / "invalid_meta.txt"
    filter_file.write_text("# invalid:format:with:colons\n# label: Valid Label\n- **/*.tmp\n")

    rules = parse_filter_file(filter_file)
    assert len(rules) == 1
    assert rules[0].label == "Valid Label"
    assert rules[0].pattern == "**/*.tmp"


def test_match_engine_very_long_path(tmp_path: Path) -> None:
    """Test that very long paths are handled correctly."""
    # Create a very long path
    long_path = tmp_path
    for i in range(20):
        long_path = long_path / f"directory_{i}_with_very_long_name"
    long_path.mkdir(parents=True)
    test_file = long_path / "test.txt"
    test_file.write_text("test")

    rules = [Rule(action="-", pattern="**/*.txt", lineno=1)]
    engine = MatchEngine(rules)

    result = engine.evaluate_path(test_file, tmp_path)
    assert result.decision.matched is True
    assert len(result.rel_path) > 200  # Ensure path is actually long


def test_parse_filter_file_whitespace_only_lines(tmp_path: Path) -> None:
    """Test that whitespace-only lines are handled correctly."""
    filter_file = tmp_path / "whitespace.txt"
    filter_file.write_text("   \n\t\n- **/*.tmp\n  \n")

    rules = parse_filter_file(filter_file)
    assert len(rules) == 1
    assert rules[0].pattern == "**/*.tmp"
