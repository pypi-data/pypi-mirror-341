"""Tests for utility functions."""

import json
import logging
from pathlib import Path
from unittest import mock

import pytest
from rich.console import Console

from taskinator.utils import (
    ensure_task_structure,
    find_task_by_id,
    read_json,
    sanitize_prompt,
    truncate,
    validate_task_id,
    write_json
)


@pytest.fixture
def sample_tasks():
    """Fixture providing sample tasks for testing."""
    return [
        {
            "id": 1,
            "title": "Task 1",
            "status": "pending",
            "description": "Test task 1"
        },
        {
            "id": 2,
            "title": "Task 2",
            "status": "in_progress",
            "description": "Test task 2"
        }
    ]


@pytest.fixture
def temp_json_file(tmp_path):
    """Fixture providing a temporary JSON file."""
    json_file = tmp_path / "test.json"
    return json_file


def test_read_json(temp_json_file, sample_tasks):
    """Test reading JSON files."""
    # Write sample data
    temp_json_file.write_text(json.dumps({"tasks": sample_tasks}))
    
    # Test reading
    data = read_json(temp_json_file)
    assert "tasks" in data
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["id"] == 1


def test_read_json_not_found():
    """Test reading non-existent JSON file."""
    with pytest.raises(FileNotFoundError):
        read_json("nonexistent.json")


def test_read_json_invalid():
    """Test reading invalid JSON file."""
    with pytest.raises(json.JSONDecodeError):
        with mock.patch("pathlib.Path.open", 
            mock.mock_open(read_data="invalid json")):
            read_json("test.json")


def test_write_json(temp_json_file, sample_tasks):
    """Test writing JSON files."""
    data = {"tasks": sample_tasks}
    write_json(temp_json_file, data)
    
    # Verify written content
    written_data = json.loads(temp_json_file.read_text())
    assert written_data == data


def test_write_json_creates_dirs(tmp_path):
    """Test write_json creates directories if needed."""
    nested_file = tmp_path / "deep" / "nested" / "test.json"
    data = {"test": "data"}
    
    write_json(nested_file, data)
    assert nested_file.exists()
    assert json.loads(nested_file.read_text()) == data


def test_sanitize_prompt():
    """Test prompt sanitization."""
    # Test basic sanitization
    assert sanitize_prompt("  test  ") == "test"
    
    # Test null character removal
    assert sanitize_prompt("test\x00data") == "testdata"
    
    # Test empty input
    assert sanitize_prompt("") == ""


def test_find_task_by_id(sample_tasks):
    """Test finding tasks by ID."""
    # Test finding existing task
    task = find_task_by_id(sample_tasks, 1)
    assert task is not None
    assert task["id"] == 1
    
    # Test with string ID
    task = find_task_by_id(sample_tasks, "2")
    assert task is not None
    assert task["id"] == 2
    
    # Test non-existent task
    assert find_task_by_id(sample_tasks, 999) is None


def test_truncate():
    """Test text truncation."""
    text = "This is a long text that needs truncation"
    
    # Test no truncation needed
    assert truncate(text, 100) == text
    
    # Test truncation
    truncated = truncate(text, 10)
    assert len(truncated) <= 10
    assert truncated.endswith("...")
    
    # Test custom suffix
    truncated = truncate(text, 10, suffix="!")
    assert truncated.endswith("!")


def test_ensure_task_structure():
    """Test task structure validation and defaults."""
    # Test minimal task
    minimal_task = {"id": 1, "title": "Test"}
    complete_task = ensure_task_structure(minimal_task)
    
    # Check defaults
    assert complete_task["status"] == "pending"
    assert complete_task["priority"] == "medium"
    assert isinstance(complete_task["dependencies"], list)
    assert isinstance(complete_task["subtasks"], list)
    assert isinstance(complete_task["created"], float)
    assert isinstance(complete_task["updated"], float)
    
    # Test with existing values
    custom_task = {
        "id": 2,
        "title": "Test 2",
        "status": "done",
        "priority": "high"
    }
    validated_task = ensure_task_structure(custom_task)
    assert validated_task["status"] == "done"
    assert validated_task["priority"] == "high"


def test_validate_task_id():
    """Test task ID validation."""
    # Test valid IDs
    assert validate_task_id(1) == "1"
    assert validate_task_id("001") == "1"
    assert validate_task_id("1") == "1"
    
    # Test invalid IDs
    with pytest.raises(ValueError):
        validate_task_id(0)
    
    with pytest.raises(ValueError):
        validate_task_id(-1)
    
    with pytest.raises(ValueError):
        validate_task_id("abc")
    
    with pytest.raises(ValueError):
        validate_task_id("")


def test_logging_setup():
    """Test logging configuration."""
    # Get the logger
    logger = logging.getLogger("taskinator")
    
    # Check logger level
    assert logger.level in (logging.INFO, logging.DEBUG)
    
    # Check handler configuration
    assert any(
        handler.__class__.__name__ == "RichHandler"
        for handler in logger.handlers
    )


def test_console_setup():
    """Test console configuration."""
    # Import console from utils
    from taskinator.utils import console
    
    # Verify it's a Rich console
    assert isinstance(console, Console)