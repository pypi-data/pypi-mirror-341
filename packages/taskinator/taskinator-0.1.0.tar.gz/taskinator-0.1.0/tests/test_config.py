"""Tests for configuration management."""

import os
from pathlib import Path
from unittest import mock

import pytest
from pydantic import ValidationError

from taskinator.config import Config, TaskPriority, TaskStatus


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    assert config.max_tokens == 4000
    assert config.temperature == 0.7
    assert config.default_subtasks == 5
    assert config.tasks_dir == Path("tasks")
    assert config.debug is False


def test_config_env_override():
    """Test environment variable overrides."""
    with mock.patch.dict(os.environ, {
        "MAX_TOKENS": "2000",
        "TEMPERATURE": "0.5",
        "DEFAULT_SUBTASKS": "3",
        "DEBUG": "true"
    }):
        config = Config()
        assert config.max_tokens == 2000
        assert config.temperature == 0.5
        assert config.default_subtasks == 3
        assert config.debug is True


def test_config_api_keys():
    """Test API key configuration."""
    with mock.patch.dict(os.environ, {
        "ANTHROPIC_API_KEY": "test-key",
        "PERPLEXITY_API_KEY": "test-key-2"
    }):
        config = Config()
        assert config.anthropic_api_key == "test-key"
        assert config.perplexity_api_key == "test-key-2"


def test_ensure_directories(tmp_path):
    """Test directory creation."""
    config = Config(tasks_dir=tmp_path / "tasks")
    config.ensure_directories()
    assert config.tasks_dir.exists()
    assert config.tasks_dir.is_dir()


def test_task_status_validation():
    """Test task status validation."""
    assert TaskStatus.is_valid(TaskStatus.PENDING)
    assert TaskStatus.is_valid(TaskStatus.IN_PROGRESS)
    assert TaskStatus.is_valid(TaskStatus.DONE)
    assert TaskStatus.is_valid(TaskStatus.BLOCKED)
    assert not TaskStatus.is_valid("invalid")


def test_task_priority_validation():
    """Test task priority validation."""
    assert TaskPriority.is_valid(TaskPriority.LOW)
    assert TaskPriority.is_valid(TaskPriority.MEDIUM)
    assert TaskPriority.is_valid(TaskPriority.HIGH)
    assert not TaskPriority.is_valid("invalid")


def test_config_validation():
    """Test configuration validation."""
    with pytest.raises(ValidationError):
        Config(temperature=2.0)  # Temperature should be between 0 and 1
    
    with pytest.raises(ValidationError):
        Config(max_tokens=-1)  # Max tokens should be positive


def test_model_names():
    """Test model name configuration."""
    config = Config()
    assert config.claude_model == "claude-3-opus-20240229"
    assert config.perplexity_model == "sonar-pro"
    
    with mock.patch.dict(os.environ, {
        "CLAUDE_MODEL": "claude-3-sonnet-20240229",
        "PERPLEXITY_MODEL": "sonar-medium-online"
    }):
        config = Config()
        assert config.claude_model == "claude-3-sonnet-20240229"
        assert config.perplexity_model == "sonar-medium-online"