"""Tests for task management functionality."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from taskinator.config import TaskStatus
from taskinator.task_manager import TaskManager


@pytest.fixture
def temp_tasks_dir(tmp_path):
    """Fixture providing a temporary tasks directory."""
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    return tasks_dir


@pytest.fixture
def sample_tasks():
    """Fixture providing sample tasks data."""
    return {
        "tasks": [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Test task 1",
                "details": "Implementation details 1",
                "status": "pending",
                "priority": "medium",
                "dependencies": [],
                "testStrategy": "Test strategy 1"
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Test task 2",
                "details": "Implementation details 2",
                "status": "in_progress",
                "priority": "high",
                "dependencies": [1],
                "testStrategy": "Test strategy 2"
            }
        ]
    }


@pytest.fixture
def task_manager(temp_tasks_dir):
    """Fixture providing a TaskManager instance."""
    return TaskManager(tasks_dir=temp_tasks_dir)


@pytest.fixture
def setup_tasks_file(temp_tasks_dir, sample_tasks):
    """Fixture to set up a tasks.json file."""
    tasks_file = temp_tasks_dir / "tasks.json"
    tasks_file.write_text(json.dumps(sample_tasks))
    return tasks_file


@pytest.mark.asyncio
async def test_parse_prd(task_manager, temp_tasks_dir):
    """Test PRD parsing functionality."""
    # Create test PRD file
    prd_file = temp_tasks_dir / "test.prd"
    prd_file.write_text("Test PRD content")
    
    # Mock AI service call
    with patch("taskinator.ai_services.call_claude") as mock_call_claude:
        mock_call_claude.return_value = {
            "tasks": [
                {
                    "id": 1,
                    "title": "Generated Task",
                    "description": "Test description",
                    "details": "Test details",
                    "status": "pending",
                    "priority": "medium",
                    "dependencies": []
                }
            ]
        }
        
        await task_manager.parse_prd(prd_file)
        
        # Verify tasks.json was created
        tasks_file = temp_tasks_dir / "tasks.json"
        assert tasks_file.exists()
        
        # Verify task file was created
        task_file = temp_tasks_dir / "task_001.txt"
        assert task_file.exists()
        
        # Verify file contents
        tasks_data = json.loads(tasks_file.read_text())
        assert len(tasks_data["tasks"]) == 1
        assert tasks_data["tasks"][0]["title"] == "Generated Task"


@pytest.mark.asyncio
async def test_generate_task_files(
    task_manager,
    temp_tasks_dir,
    setup_tasks_file,
    sample_tasks
):
    """Test task file generation."""
    await task_manager.generate_task_files()
    
    # Verify task files were created
    for task in sample_tasks["tasks"]:
        task_file = temp_tasks_dir / f"task_{str(task['id']).zfill(3)}.txt"
        assert task_file.exists()
        
        # Verify file contents
        content = task_file.read_text()
        assert f"Task ID: {task['id']}" in content
        assert f"Title: {task['title']}" in content
        assert task['description'] in content


@pytest.mark.asyncio
async def test_update_tasks(task_manager, setup_tasks_file):
    """Test task updating functionality."""
    with patch("taskinator.ai_services.update_tasks") as mock_update:
        mock_update.return_value = [
            {
                "id": 1,
                "title": "Updated Task",
                "description": "Updated description",
                "status": "in_progress",
                "priority": "high",
                "dependencies": []
            }
        ]
        
        await task_manager.update_tasks(1, "Update context")
        
        # Verify tasks were updated
        tasks_data = json.loads(task_manager.tasks_file.read_text())
        updated_task = next(t for t in tasks_data["tasks"] if t["id"] == 1)
        assert updated_task["title"] == "Updated Task"
        assert updated_task["status"] == "in_progress"


@pytest.mark.asyncio
async def test_set_task_status(task_manager, setup_tasks_file):
    """Test setting task status."""
    await task_manager.set_task_status("1", TaskStatus.DONE)
    
    # Verify status was updated
    tasks_data = json.loads(task_manager.tasks_file.read_text())
    updated_task = next(t for t in tasks_data["tasks"] if t["id"] == 1)
    assert updated_task["status"] == TaskStatus.DONE
    
    # Verify dependent task was updated
    dependent_task = next(t for t in tasks_data["tasks"] if t["id"] == 2)
    assert dependent_task["status"] == TaskStatus.PENDING


def test_list_tasks(task_manager, setup_tasks_file, capsys):
    """Test task listing functionality."""
    # Test listing all tasks
    task_manager.list_tasks()
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out
    
    # Test filtering by status
    task_manager.list_tasks(status_filter="in_progress")
    captured = capsys.readouterr()
    assert "Task 1" not in captured.out
    assert "Task 2" in captured.out


@pytest.mark.asyncio
async def test_expand_task(task_manager, setup_tasks_file):
    """Test task expansion functionality."""
    with patch("taskinator.ai_services.generate_subtasks") as mock_generate:
        mock_generate.return_value = [
            {
                "id": 1,
                "title": "Subtask 1",
                "description": "Test subtask",
                "status": "pending",
                "dependencies": []
            }
        ]
        
        await task_manager.expand_task(1)
        
        # Verify subtasks were added
        tasks_data = json.loads(task_manager.tasks_file.read_text())
        expanded_task = next(t for t in tasks_data["tasks"] if t["id"] == 1)
        assert "subtasks" in expanded_task
        assert len(expanded_task["subtasks"]) == 1
        assert expanded_task["subtasks"][0]["title"] == "Subtask 1"


@pytest.mark.asyncio
async def test_error_handling(task_manager, temp_tasks_dir):
    """Test error handling in task operations."""
    # Test parsing non-existent PRD
    with pytest.raises(FileNotFoundError):
        await task_manager.parse_prd(temp_tasks_dir / "nonexistent.prd")
    
    # Test invalid task ID
    with pytest.raises(ValueError):
        await task_manager.set_task_status("invalid", TaskStatus.DONE)
    
    # Test invalid status
    with pytest.raises(ValueError):
        await task_manager.set_task_status("1", "invalid_status")


@pytest.mark.asyncio
async def test_task_file_formatting(task_manager, setup_tasks_file):
    """Test task file content formatting."""
    await task_manager.generate_task_files()
    
    task_file = task_manager.tasks_dir / "task_001.txt"
    content = task_file.read_text()
    
    # Verify sections
    assert "# Task ID:" in content
    assert "# Title:" in content
    assert "# Status:" in content
    assert "# Priority:" in content
    assert "# Description:" in content
    assert "# Details:" in content
    assert "# Test Strategy:" in content
    
    # Verify formatting
    lines = content.split("\n")
    assert all(
        line.startswith("#") or not line.strip() or line.startswith(" ")
        for line in lines
    )


@pytest.mark.asyncio
async def test_concurrent_operations(task_manager, setup_tasks_file):
    """Test handling of concurrent task operations."""
    # Test concurrent status updates
    status_updates = []
    for task_id in ["1", "2"]:
        status_updates.append(
            task_manager.set_task_status(task_id, TaskStatus.IN_PROGRESS)
        )
    
    await asyncio.gather(*status_updates)
    
    # Verify all updates were applied
    tasks_data = json.loads(task_manager.tasks_file.read_text())
    assert all(
        task["status"] == TaskStatus.IN_PROGRESS
        for task in tasks_data["tasks"]
    )