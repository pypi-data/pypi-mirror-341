"""NextCloud adapter for external integration."""

import json
import re
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import uuid

from taskinator.nextcloud_client import NextCloudClient, NextCloudTask
from taskinator.sync_metadata_store import SyncMetadataStore
from taskinator.constants import SyncStatus, ExternalSystem

log = logging.getLogger(__name__)

# Constants for sync status
# class SyncStatus:
#     """Synchronization status constants."""
#     SYNCED = "synced"
#     ERROR = "error"
#     CONFLICT = "conflict"
#     SKIPPED = "skipped"
#     PENDING = "pending"

# Constants for external systems
# class ExternalSystem:
#     """External system constants."""
#     NEXTCLOUD = "nextcloud"

class NextCloudAdapter:
    """Adapter for NextCloud integration."""
    
    # Mapping from Taskinator fields to NextCloud fields
    LOCAL_TO_REMOTE = {
        "title": "title",
        "description": "description",
        "status": "status",  # Special handling required
        "due_date": "due_date",
        "priority": "priority",  # Special handling required
    }
    
    # Mapping from NextCloud fields to Taskinator fields
    REMOTE_TO_LOCAL = {
        "title": "title",
        "description": "description",
        "status": "status",  # Special handling required
        "due_date": "due_date",
        "priority": "priority",  # Special handling required
    }
    
    def __init__(
        self, 
        host: str, 
        username: str, 
        password: str = None, 
        token: str = None,
        calendar_name: str = "Taskinator",
        metadata_store: SyncMetadataStore = None,
        verbose: bool = False
    ):
        """Initialize NextCloud adapter.
        
        Args:
            host: NextCloud host
            username: NextCloud username
            password: NextCloud password
            token: NextCloud token
            calendar_name: Name of the calendar to use for tasks
            metadata_store: Sync metadata store
            verbose: Enable verbose logging
        """
        self.host = host
        self.username = username
        self.password = password
        self.token = token
        self.calendar_name = calendar_name
        self.metadata_store = metadata_store
        self.verbose = verbose
        
        # Create NextCloud client
        self.client = NextCloudClient(
            host=host,
            username=username,
            password=password,
            token=token,
            calendar_name=calendar_name,  # Pass calendar_name to the client
            verbose=verbose
        )
        
    async def initialize(self):
        """Initialize the adapter.
        
        This method should be called after creating the adapter to ensure
        the calendar is set up correctly.
        
        Returns:
            Calendar object if successfully created/found, None otherwise
        """
        # Initialize the client
        await self.client.initialize()
        
        # Check if the calendar exists, create it if it doesn't
        calendar = await self.get_or_create_calendar(self.calendar_name)
        
        if calendar:
            # Set the calendar ID in the client
            self.client.calendar_id = calendar.id
            log.info(f"Using calendar '{self.calendar_name}' with ID {calendar.id}")
        else:
            log.error(f"Failed to get or create calendar '{self.calendar_name}'")
        
        return calendar
            
    async def get_or_create_calendar(self, calendar_name: str) -> Optional[Dict[str, Any]]:
        """Get or create a calendar with the given name.
        
        Args:
            calendar_name: Name of the calendar
            
        Returns:
            Calendar object if found or created, None otherwise
        """
        try:
            # Get all calendars
            calendars = await self.client.get_calendars()
            
            # Normalize the calendar name for robust comparison
            def norm(name):
                return name.strip().lower() if isinstance(name, str) else ""
            target = norm(calendar_name)

            # Look for a calendar with the given name (case-insensitive, trimmed)
            for calendar in calendars:
                if norm(calendar.display_name) == target:
                    log.info(f"Found existing calendar '{calendar.display_name}' with ID {calendar.id}")
                    return calendar
            
            # Calendar not found, create it
            log.info(f"Creating new calendar '{calendar_name}'")
            calendar = await self.client.create_calendar(calendar_name)
            
            if calendar:
                log.info(f"Created calendar '{calendar.display_name}' with ID {calendar.id}")
                return calendar
            else:
                log.error(f"Failed to create calendar '{calendar_name}'")
                return None
                
        except Exception as e:
            log.error(f"Error getting or creating calendar '{calendar_name}': {e}")
            return None
    
    async def sync_task(self, task: Dict[str, Any], direction: str = "bidirectional") -> Dict[str, Any]:
        """Synchronize a task with NextCloud.
        
        Args:
            task: Taskinator task
            direction: Synchronization direction (bidirectional, local_to_remote, remote_to_local)
            
        Returns:
            Updated task with sync metadata
        """
        # Get NextCloud metadata
        metadata = next((m for m in task.get("external_sync", []) if isinstance(m, dict) and m.get("system") == ExternalSystem.NEXTCLOUD), {})
        
        if direction == "local_to_remote":
            return await self._sync_local_to_remote(task, metadata)
        elif direction == "remote_to_local":
            return await self._sync_remote_to_local(task, metadata)
        else:  # bidirectional
            # First check if there's a remote task
            if metadata.get("external_id"):
                # Get remote task
                try:
                    remote_task = await self.client.get_task(metadata["external_id"])
                    
                    # Detect changes
                    remote_dict = self.map_remote_to_local(remote_task)
                    changes, has_conflict = self._detect_changes(task, remote_dict)
                    
                    if has_conflict:
                        # Handle conflict
                        log.warning(f"Conflict detected for task {task['id']}")
                        metadata["sync_status"] = SyncStatus.CONFLICT
                        return self._update_task_metadata(task, metadata)
                    
                    if changes:
                        # Apply changes based on which side was updated more recently
                        local_updated = task.get("updated", 0) or 0  # Ensure not None
                        remote_updated = 0
                        
                        # Convert remote timestamp to comparable format
                        if remote_task.updated_at:
                            try:
                                # If it's a string ISO format, convert to timestamp
                                if isinstance(remote_task.updated_at, str):
                                    remote_updated = datetime.fromisoformat(remote_task.updated_at).timestamp()
                                # If it's already a timestamp
                                elif isinstance(remote_task.updated_at, (int, float)):
                                    remote_updated = float(remote_task.updated_at)
                            except (ValueError, TypeError):
                                # If conversion fails, use current time
                                remote_updated = datetime.now().timestamp()
                        
                        if self.verbose:
                            log.info(f"Task {task['id']} - Local updated: {local_updated}, Remote updated: {remote_updated}")
                            
                        if local_updated > remote_updated:
                            if self.verbose:
                                log.info(f"Task {task['id']} - Local is newer, syncing to remote")
                            return await self._sync_local_to_remote(task, metadata)
                        else:
                            if self.verbose:
                                log.info(f"Task {task['id']} - Remote is newer, syncing to local")
                            return await self._sync_remote_to_local(task, metadata)
                    
                    # No changes, task is in sync
                    metadata["sync_status"] = SyncStatus.SYNCED
                    return self._update_task_metadata(task, metadata)
                    
                except Exception as e:
                    import traceback
                    log.error(f"Error syncing task {task['id']} with NextCloud: {e}")
                    log.debug(f"Traceback: {traceback.format_exc()}")
                    
                    # Check if the error is because the task doesn't exist
                    if "not found" in str(e):
                        log.warning(f"Task {task['id']} not found in NextCloud, creating a new one")
                        # Clear the external ID so a new task will be created
                        metadata["external_id"] = None
                        return await self._sync_local_to_remote(task, metadata)
                    else:
                        # For other errors, mark as error
                        metadata["sync_status"] = SyncStatus.ERROR
                        return self._update_task_metadata(task, metadata)
            else:
                # No remote task, create one
                return await self._sync_local_to_remote(task, metadata)
                
    async def _sync_local_to_remote(self, task: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize a task from local to remote.
        
        Args:
            task: Taskinator task
            metadata: External sync metadata
            
        Returns:
            Updated task
        """
        try:
            # Map task to NextCloud format
            remote_data = self.map_local_to_remote(task)
            
            # Extract subtasks to handle them separately
            subtasks_data = []
            if "subtasks" in task and task["subtasks"]:
                for subtask in task["subtasks"]:
                    if isinstance(subtask, dict):
                        subtasks_data.append(subtask)
                    else:
                        # If it's just an ID, try to find the full subtask data
                        # This would require access to the task manager
                        pass
            
            # Check if we have an external ID
            if metadata.get("external_id"):
                # Update existing task
                log.info(f"Updating task {task['id']} in NextCloud")
                remote_task = await self.client.update_task(metadata["external_id"], remote_data)
                
                # Handle subtasks
                if subtasks_data:
                    try:
                        # Create subtasks using the parent-child relationship
                        for subtask_data in subtasks_data:
                            # Format subtask data with proper title and description
                            subtask_title = f"{task['id']}.{subtask_data.get('id', '')}: {subtask_data.get('title', 'Untitled Subtask')}"
                            
                            # Create formatted description for subtask
                            subtask_description = self._format_subtask_description(subtask_data, task['id'])
                            
                            subtask_remote_data = {
                                "title": subtask_title,
                                "description": subtask_description,
                                "status": self._map_status_to_remote(subtask_data.get("status", "pending"))
                            }
                            
                            # Create subtask with parent ID
                            await self.client.create_task(subtask_remote_data, parent_id=metadata["external_id"])
                    except Exception as e:
                        log.warning(f"Error handling subtasks for task {task['id']}: {e}")
            else:
                # Create new task
                log.info(f"Creating task {task['id']} in NextCloud")
                remote_task = await self.client.create_task(remote_data)
                
                # Store external ID
                metadata["external_id"] = remote_task.id
                
                # Handle subtasks
                if subtasks_data:
                    try:
                        # Create subtasks using the parent-child relationship
                        for subtask_data in subtasks_data:
                            # Format subtask data with proper title and description
                            subtask_title = f"{task['id']}.{subtask_data.get('id', '')}: {subtask_data.get('title', 'Untitled Subtask')}"
                            
                            # Create formatted description for subtask
                            subtask_description = self._format_subtask_description(subtask_data, task['id'])
                            
                            subtask_remote_data = {
                                "title": subtask_title,
                                "description": subtask_description,
                                "status": self._map_status_to_remote(subtask_data.get("status", "pending"))
                            }
                            
                            # Create subtask with parent ID
                            await self.client.create_task(subtask_remote_data, parent_id=remote_task.id)
                    except Exception as e:
                        log.warning(f"Error creating subtasks for task {task['id']}: {e}")
            
            # Update metadata
            metadata["external_url"] = f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{remote_task.id}"
            metadata["etag"] = remote_task.etag or ""
            metadata["last_sync"] = datetime.now().timestamp()
            metadata["sync_status"] = SyncStatus.SYNCED
            
            # Return updated task with metadata
            if "external_sync" not in task:
                task["external_sync"] = []
                
            # Remove any existing metadata for this system
            task["external_sync"] = [
                m for m in task["external_sync"] 
                if isinstance(m, dict) and m.get("system") != ExternalSystem.NEXTCLOUD
            ]
            
            # Add updated metadata
            task["external_sync"].append(metadata)
            
            return task
            
        except Exception as e:
            import traceback
            log.error(f"Error syncing task {task['id']} to NextCloud: {e}")
            log.debug(f"Traceback: {traceback.format_exc()}")
            metadata["sync_status"] = SyncStatus.ERROR
            
            # Return task with error metadata
            if "external_sync" not in task:
                task["external_sync"] = []
                
            # Remove any existing metadata for this system
            task["external_sync"] = [
                m for m in task["external_sync"] 
                if isinstance(m, dict) and m.get("system") != ExternalSystem.NEXTCLOUD
            ]
            
            # Add updated metadata
            task["external_sync"].append(metadata)
            
            return task
    
    async def _sync_remote_to_local(self, remote_task: NextCloudTask, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize a task from remote to local.
        
        Args:
            remote_task: NextCloud task
            metadata: External sync metadata
            
        Returns:
            Updated task
        """
        try:
            # Map remote task to local format
            local_task = self.map_remote_to_local(remote_task)
            
            # Check if this is a subtask
            is_subtask = False
            parent_id = None
            
            # Check if this task has a RELATED-TO relationship
            if remote_task.related_to:
                is_subtask = True
                parent_task = await self.client.get_task(remote_task.related_to)
                if parent_task:
                    # Try to find the parent task ID in our system
                    parent_metadata = self.metadata_store.find_by_external_id(
                        ExternalSystem.NEXTCLOUD, 
                        parent_task.id
                    )
                    if parent_metadata:
                        parent_id = parent_metadata.get("task_id")
            
            # If this is a subtask and we found the parent, handle differently
            if is_subtask and parent_id:
                # This is a subtask, we'll handle it through the parent task
                log.info(f"Task {remote_task.id} is a subtask of {parent_id}, will be handled through parent")
                
                # Update metadata to indicate this is a subtask
                metadata["is_subtask"] = True
                metadata["parent_id"] = parent_id
                metadata["external_id"] = remote_task.id
                metadata["external_url"] = f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{remote_task.id}"
                metadata["etag"] = remote_task.etag or ""
                metadata["last_sync"] = datetime.now().timestamp()
                metadata["sync_status"] = SyncStatus.SYNCED
                
                # Return a minimal task with metadata
                task = {
                    "id": f"{parent_id}.{local_task.get('id', '')}",
                    "title": local_task.get("title", ""),
                    "status": local_task.get("status", "pending"),
                    "external_sync": [metadata]
                }
                
                return task
            
            # Regular task (not a subtask)
            # Get subtasks for this task
            subtasks = []
            try:
                # Get subtasks by checking for tasks with RELATED-TO relationship
                remote_subtasks = await self.client.get_subtasks(remote_task.id)
                
                if remote_subtasks:
                    for subtask in remote_subtasks:
                        # Map the subtask to local format
                        local_subtask = self.map_remote_to_local(subtask)
                        
                        # Create subtask ID based on parent ID
                        if "id" in local_task:
                            # Extract the numeric part after the dot if it exists
                            subtask_id_match = re.search(r'(\d+)$', local_subtask.get("id", ""))
                            if subtask_id_match:
                                subtask_id = subtask_id_match.group(1)
                            else:
                                # Generate a unique ID for the subtask
                                subtask_id = str(uuid.uuid4())[:8]
                                
                            local_subtask["id"] = subtask_id
                        
                        # Add subtask metadata
                        subtask_metadata = {
                            "system": ExternalSystem.NEXTCLOUD,
                            "external_id": subtask.id,
                            "external_url": f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{subtask.id}",
                            "etag": subtask.etag or "",
                            "last_sync": datetime.now().timestamp(),
                            "sync_status": SyncStatus.SYNCED,
                            "is_subtask": True,
                            "parent_id": local_task.get("id", "")
                        }
                        
                        if "external_sync" not in local_subtask:
                            local_subtask["external_sync"] = []
                            
                        local_subtask["external_sync"].append(subtask_metadata)
                        
                        subtasks.append(local_subtask)
            except Exception as e:
                log.warning(f"Error getting subtasks for task {remote_task.id}: {e}")
            
            # Add subtasks to the task
            if subtasks:
                local_task["subtasks"] = subtasks
            
            # Update metadata
            metadata["external_id"] = remote_task.id
            metadata["external_url"] = f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{remote_task.id}"
            metadata["etag"] = remote_task.etag or ""
            metadata["last_sync"] = datetime.now().timestamp()
            metadata["sync_status"] = SyncStatus.SYNCED
            
            # Add metadata to the task
            if "external_sync" not in local_task:
                local_task["external_sync"] = []
                
            local_task["external_sync"].append(metadata)
            
            return local_task
            
        except Exception as e:
            import traceback
            log.error(f"Error syncing task {remote_task.id} from NextCloud: {e}")
            log.debug(f"Traceback: {traceback.format_exc()}")
            
            # Create a minimal task with error metadata
            metadata["sync_status"] = SyncStatus.ERROR
            
            task = {
                "title": remote_task.title,
                "external_sync": [metadata]
            }
            
            return task

    async def get_external_task(self, external_id: str) -> Optional[NextCloudTask]:
        """Get a task from NextCloud by its ID.
        
        Args:
            external_id: External task ID
            
        Returns:
            NextCloud task if found, None otherwise
        """
        try:
            # Get task from NextCloud
            task = await self.client.get_task(external_id)
            return task
        except Exception as e:
            log.error(f"Error getting task {external_id} from NextCloud: {e}")
            return None

    def map_local_to_remote(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Map a local task to a remote task.
        
        Args:
            task: Local task
            
        Returns:
            Remote task
        """
        # Include task ID in the title
        task_id = task.get("id", "")
        title = f"{task_id}: {task.get('title', '')}"
        
        remote_task = {
            "title": title,
            "status": self._map_status_to_remote(task.get("status", "pending")),
            "priority": self._map_priority_to_remote(task.get("priority", "medium")),
        }
        
        # Add due date if present
        if task.get("due_date"):
            remote_task["due_date"] = task["due_date"]
            
        # Add categories for dependencies
        categories = []
        
        # Add dependencies as categories
        if "dependencies" in task and task["dependencies"]:
            for dep_id in task["dependencies"]:
                categories.append(f"Depends on: {dep_id}")
                
        if categories:
            remote_task["categories"] = categories
            
        # Format description with Markdown to include all task details
        description = ""
        
        # Create a formatted task details box
        description += "```markdown\n"
        description += "# Task Details\n\n"
        
        # Add task header
        description += f"## {task_id}: {task.get('title', '')}\n\n"
        
        # Add status and priority
        description += f"**Status:** {task.get('status', 'pending')}\n"
        description += f"**Priority:** {task.get('priority', 'medium')}\n"
        
        # Add dependencies if present
        if "dependencies" in task and task["dependencies"]:
            deps_str = ", ".join(str(dep) for dep in task["dependencies"])
            description += f"**Dependencies:** {deps_str}\n"
        
        description += "\n"
        
        # Add description section
        if task.get("description"):
            description += "## Description\n\n"
            description += f"{task.get('description')}\n\n"
        
        # Add details section
        if task.get("details"):
            description += "## Details\n\n"
            description += f"{task.get('details')}\n\n"
        
        # Add test strategy section
        if task.get("test_strategy"):
            description += "## Test Strategy\n\n"
            description += f"{task.get('test_strategy')}\n\n"
        
        description += "```\n"
        
        # Store the formatted description
        remote_task["description"] = description
        
        if self.verbose:
            log.info(f"Mapped local task {task.get('id')} to remote format")
            
        return remote_task
    
    def map_remote_to_local(self, remote_task: NextCloudTask) -> Dict[str, Any]:
        """Map NextCloud task to Taskinator task.
        
        Args:
            remote_task: NextCloud task
            
        Returns:
            Dictionary with Taskinator task fields
        """
        # Create basic task structure
        local_task = {
            "status": self._map_status_to_local(remote_task.status),
            "priority": self._map_priority_to_local(remote_task.priority)
        }
        
        # Extract task ID and title from the remote task title
        title = remote_task.title
        task_id = None
        
        # Try to extract task ID from title (format: "6: Title")
        import re
        id_match = re.match(r"(\d+(?:\.\d+)*): (.*)", title)
        if id_match:
            task_id = id_match.group(1)
            title = id_match.group(2)
        
        # Set the title without the task ID prefix
        local_task["title"] = title
        
        # Parse description to extract structured task details
        description = remote_task.description or ""
        
        # Check if the description is in our structured Markdown format
        if "```markdown" in description and "# Task Details" in description:
            # Extract sections from the Markdown
            try:
                # Extract description section
                desc_match = re.search(r"## Description\n\n(.*?)(?=\n\n##|\n\n```|$)", description, re.DOTALL)
                if desc_match:
                    local_task["description"] = desc_match.group(1).strip()
                
                # Extract details section
                details_match = re.search(r"## Details\n\n(.*?)(?=\n\n##|\n\n```|$)", description, re.DOTALL)
                if details_match:
                    local_task["details"] = details_match.group(1).strip()
                
                # Extract test strategy section
                test_strategy_match = re.search(r"## Test Strategy\n\n(.*?)(?=\n\n##|\n\n```|$)", description, re.DOTALL)
                if test_strategy_match:
                    local_task["test_strategy"] = test_strategy_match.group(1).strip()
                
                # Extract dependencies from the Markdown
                deps_match = re.search(r"\*\*Dependencies:\*\* (.*?)(?=\n)", description)
                if deps_match:
                    deps_str = deps_match.group(1).strip()
                    try:
                        # Parse comma-separated list of dependencies
                        deps = [int(dep.strip()) for dep in deps_str.split(",")]
                        if deps:
                            local_task["dependencies"] = deps
                    except ValueError:
                        # If parsing fails, try to extract from categories
                        pass
            except Exception as e:
                log.warning(f"Error parsing structured Markdown: {e}")
        else:
            # If not in our structured format, use the whole description
            local_task["description"] = description.strip()
        
        # Add due date if present
        if remote_task.due_date:
            local_task["due_date"] = remote_task.due_date
            
        # Extract dependencies from categories if not already set
        if "dependencies" not in local_task:
            dependencies = []
            for category in remote_task.categories:
                if category.startswith("Depends on: "):
                    dep_id = category.replace("Depends on: ", "")
                    try:
                        dependencies.append(int(dep_id))
                    except ValueError:
                        # If it's not a valid integer, skip it
                        pass
                        
            if dependencies:
                local_task["dependencies"] = dependencies
            
        if self.verbose:
            log.info(f"Mapped remote task {remote_task.id} to local format")
            if "dependencies" in local_task:
                log.info(f"  Dependencies: {local_task['dependencies']}")
                
        return local_task

    def _map_status_to_remote(self, status: str) -> str:
        """Map Taskinator status to NextCloud status.
        
        Args:
            status: Taskinator status
            
        Returns:
            NextCloud status
        """
        if status == "done":
            return "COMPLETED"
        elif status == "in_progress":
            return "IN-PROCESS"
        elif status == "blocked":
            return "CANCELLED"
        else:
            return "NEEDS-ACTION"
    
    def _map_status_to_local(self, status: str) -> str:
        """Map NextCloud status to Taskinator status.
        
        Args:
            status: NextCloud status
            
        Returns:
            Taskinator status
        """
        if status == "COMPLETED":
            return "done"
        elif status == "IN-PROCESS":
            return "in_progress"
        elif status == "CANCELLED":
            return "blocked"
        else:
            return "pending"
    
    def _map_priority_to_remote(self, priority: str) -> int:
        """Map Taskinator priority to NextCloud priority.
        
        Args:
            priority: Taskinator priority
            
        Returns:
            NextCloud priority
        """
        if priority == "high":
            return 1
        elif priority == "medium":
            return 5
        else:
            return 9
    
    def _map_priority_to_local(self, priority: Any) -> str:
        """Map NextCloud priority to Taskinator priority.
        
        Args:
            priority: NextCloud priority
            
        Returns:
            Taskinator priority
        """
        if priority is None:
            return "medium"
            
        try:
            priority_int = int(priority)
            if priority_int <= 3:
                return "high"
            elif priority_int <= 6:
                return "medium"
            else:
                return "low"
        except (ValueError, TypeError):
            return "medium"

    def _detect_changes(self, local_task: Dict[str, Any], remote_task: Dict[str, Any]) -> tuple:
        """Detect changes between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            Tuple of (changes, has_conflict)
        """
        changes = False
        has_conflict = False
        
        # Check for changes in basic fields
        for field in ["title", "description", "status", "priority", "details", "test_strategy"]:
            if field in remote_task and field in local_task:
                if remote_task[field] != local_task[field]:
                    changes = True
                    # Check for conflicts (both sides changed)
                    if field in ["title", "description", "details", "test_strategy"]:
                        has_conflict = True
        
        return changes, has_conflict
    
    def _update_task_metadata(self, task: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Update task with metadata.
        
        Args:
            task: Task to update
            metadata: Metadata to add
            
        Returns:
            Updated task
        """
        # Ensure task has external_sync field
        if "external_sync" not in task:
            task["external_sync"] = []
            
        # Remove any existing metadata for this system
        task["external_sync"] = [
            m for m in task["external_sync"] 
            if isinstance(m, dict) and m.get("system") != ExternalSystem.NEXTCLOUD
        ]
        
        # Add updated metadata
        task["external_sync"].append(metadata)
        
        return task

    def _format_subtask_description(self, subtask_data: Dict[str, Any], parent_id: str) -> str:
        """Format subtask description with Markdown.
        
        Args:
            subtask_data: Subtask data
            parent_id: Parent task ID
            
        Returns:
            Formatted description
        """
        # Format description with Markdown to include all subtask details
        description = ""
        
        # Create a formatted task details box
        description += "```markdown\n"
        description += "# Subtask Details\n\n"
        
        # Add subtask header with parent reference
        subtask_id = subtask_data.get("id", "")
        full_id = f"{parent_id}.{subtask_id}"
        description += f"## {full_id}: {subtask_data.get('title', '')}\n\n"
        
        # Add status and priority
        description += f"**Status:** {subtask_data.get('status', 'pending')}\n"
        description += f"**Priority:** {subtask_data.get('priority', 'medium')}\n"
        description += f"**Parent Task:** {parent_id}\n"
        
        description += "\n"
        
        # Add description section
        if subtask_data.get("description"):
            description += "## Description\n\n"
            description += f"{subtask_data.get('description')}\n\n"
        
        # Add details section
        if subtask_data.get("details"):
            description += "## Details\n\n"
            description += f"{subtask_data.get('details')}\n\n"
        
        description += "```\n"
        
        return description
