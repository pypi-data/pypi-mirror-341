"""Tests for the Netflix Open Content Helper package."""

import pytest

from netflix_open_content_helper.parser import parse_shotfile


def test_parser_handles_yaml_format() -> None:
    """Test that the parser handles YAML file format."""
    result = parse_shotfile("tests/test_data/one_shot.yaml")
    assert len(result) == 1
    assert result[0].project == "sparks"


def test_parser_handles_json_format() -> None:
    """Test that the parser handles JSON file format."""
    result = parse_shotfile("tests/test_data/one_shot.json")
    assert len(result) == 1
    assert result[0].frame_start == 5000


def test_parser_handles_csv_format() -> None:
    """Test that the parser handles CSV file format."""
    result = parse_shotfile("tests/test_data/one_shot.csv")
    assert len(result) == 1
    assert result[0].frame_end == 5001


def test_parser_flags_unsupported_formats() -> None:
    """Test that the parser raises an error for unsupported file formats."""
    with pytest.raises(ValueError) as excinfo:
        parse_shotfile("tests/test_data/shotfile.txt")
    assert "Unknown file type: tests/test_data/shotfile.txt" in str(excinfo.value)
