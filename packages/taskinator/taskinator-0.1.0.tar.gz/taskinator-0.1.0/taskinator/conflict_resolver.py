"""Conflict resolution for NextCloud task synchronization."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from .nextcloud_client import NextCloudTask
from .nextcloud_sync import (
    NextCloudSyncMetadata,
    SyncDirection,
    SyncStatus,
    TaskFieldMapping,
    get_nextcloud_metadata,
    update_nextcloud_metadata
)
from .utils import log


class ConflictResolutionStrategy(str, Enum):
    """Strategy for resolving conflicts."""
    LOCAL_WINS = "local_wins"
    REMOTE_WINS = "remote_wins"
    NEWEST_WINS = "newest_wins"
    MANUAL = "manual"


class ConflictResolver:
    """Handles conflict detection and resolution between local and remote tasks."""
    
    def __init__(self, default_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.NEWEST_WINS):
        """Initialize conflict resolver.
        
        Args:
            default_strategy: Default strategy for resolving conflicts
        """
        self.default_strategy = default_strategy
    
    def detect_conflict(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask
    ) -> bool:
        """Detect if there is a conflict between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            True if there is a conflict, False otherwise
        """
        # Get metadata
        metadata = get_nextcloud_metadata(local_task)
        last_sync = metadata.last_sync
        
        # Check if both sides were modified since last sync
        local_modified = local_task.get("updated", 0) > last_sync
        
        remote_modified = False
        if remote_task.modified:
            remote_modified = remote_task.modified.timestamp() > last_sync
        
        return local_modified and remote_modified
    
    def resolve_conflict(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask,
        strategy: Optional[ConflictResolutionStrategy] = None
    ) -> Tuple[Dict[str, Any], bool]:
        """Resolve conflict between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            strategy: Strategy for resolving the conflict
            
        Returns:
            Tuple of (resolved task, was_conflict)
        """
        # Use default strategy if none provided
        if strategy is None:
            strategy = self.default_strategy
        
        # Check if there's a conflict
        if not self.detect_conflict(local_task, remote_task):
            return local_task, False
        
        # Get metadata
        metadata = get_nextcloud_metadata(local_task)
        
        # Mark as conflict in metadata
        metadata.sync_status = SyncStatus.CONFLICT
        
        # Convert remote task to local format for comparison
        remote_dict = TaskFieldMapping.map_remote_to_local(remote_task)
        
        # Track changes for version history
        changes = []
        
        # Resolve based on strategy
        resolved_task = local_task.copy()
        if strategy == ConflictResolutionStrategy.LOCAL_WINS:
            # Local wins, just update metadata
            log.info(f"Conflict resolved with LOCAL_WINS for task {local_task.get('id')}")
            
            # Record changes that were overridden
            for field in TaskFieldMapping.LOCAL_TO_REMOTE.keys():
                if field in local_task and field in remote_dict and local_task[field] != remote_dict[field]:
                    changes.append({
                        "field": field,
                        "local_value": local_task[field],
                        "remote_value": remote_dict[field],
                        "resolution": "local"
                    })
            
        elif strategy == ConflictResolutionStrategy.REMOTE_WINS:
            # Remote wins, update local task with remote values
            log.info(f"Conflict resolved with REMOTE_WINS for task {local_task.get('id')}")
            
            for field in TaskFieldMapping.LOCAL_TO_REMOTE.keys():
                if field in remote_dict:
                    # Record change if values differ
                    if field in local_task and local_task[field] != remote_dict[field]:
                        changes.append({
                            "field": field,
                            "local_value": local_task[field],
                            "remote_value": remote_dict[field],
                            "resolution": "remote"
                        })
                    
                    # Update with remote value
                    resolved_task[field] = remote_dict[field]
            
        elif strategy == ConflictResolutionStrategy.NEWEST_WINS:
            # Compare timestamps and use newest values
            log.info(f"Conflict resolved with NEWEST_WINS for task {local_task.get('id')}")
            
            local_updated = local_task.get("updated", 0)
            remote_updated = remote_task.modified.timestamp() if remote_task.modified else 0
            
            for field in TaskFieldMapping.LOCAL_TO_REMOTE.keys():
                if field in local_task and field in remote_dict and local_task[field] != remote_dict[field]:
                    # Determine which version is newer
                    if local_updated > remote_updated:
                        # Local is newer
                        resolution = "local"
                        value = local_task[field]
                    else:
                        # Remote is newer
                        resolution = "remote"
                        value = remote_dict[field]
                        resolved_task[field] = value
                    
                    changes.append({
                        "field": field,
                        "local_value": local_task[field],
                        "remote_value": remote_dict[field],
                        "resolution": resolution
                    })
        
        else:  # MANUAL
            # For manual resolution, we just mark the conflict and let the user handle it
            log.info(f"Conflict marked for MANUAL resolution for task {local_task.get('id')}")
            
            # Record all differences for manual resolution
            for field in TaskFieldMapping.LOCAL_TO_REMOTE.keys():
                if field in local_task and field in remote_dict and local_task[field] != remote_dict[field]:
                    changes.append({
                        "field": field,
                        "local_value": local_task[field],
                        "remote_value": remote_dict[field],
                        "resolution": "manual"
                    })
        
        # Add version entry to track the conflict and resolution
        if changes:
            metadata.add_version(
                changes=changes,
                modified_by=f"conflict_resolution_{strategy.value}"
            )
        
        # Update metadata in the resolved task
        resolved_task = update_nextcloud_metadata(resolved_task, metadata)
        
        # Update timestamp
        resolved_task["updated"] = datetime.now().timestamp()
        
        return resolved_task, True
    
    def get_conflicts(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get all tasks with conflicts.
        
        Args:
            tasks: List of tasks
            
        Returns:
            List of tasks with conflicts
        """
        return [
            task for task in tasks
            if "nextcloud" in task and task["nextcloud"].get("sync_status") == SyncStatus.CONFLICT.value
        ]


class ManualConflictResolver:
    """Handles manual resolution of conflicts."""
    
    def resolve_field_conflict(
        self,
        task: Dict[str, Any],
        field: str,
        resolution: str  # 'local' or 'remote'
    ) -> Dict[str, Any]:
        """Resolve a specific field conflict.
        
        Args:
            task: Task with conflict
            field: Field name to resolve
            resolution: Resolution choice ('local' or 'remote')
            
        Returns:
            Updated task
        """
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        # Find the conflict in version history
        conflict_version = None
        for version in reversed(metadata.version_history):
            changes = version.get("changes", [])
            for change in changes:
                if change.get("field") == field and change.get("resolution") == "manual":
                    conflict_version = version
                    break
            if conflict_version:
                break
        
        if not conflict_version:
            log.warning(f"No manual conflict found for field {field} in task {task.get('id')}")
            return task
        
        # Update the task based on resolution
        updated_task = task.copy()
        
        # Find the change for this field
        for change in conflict_version.get("changes", []):
            if change.get("field") == field:
                if resolution == "local":
                    # Keep local value (already in the task)
                    change["resolution"] = "local"
                else:
                    # Use remote value
                    updated_task[field] = change.get("remote_value")
                    change["resolution"] = "remote"
        
        # Check if all conflicts are resolved
        all_resolved = True
        for version in metadata.version_history:
            for change in version.get("changes", []):
                if change.get("resolution") == "manual":
                    all_resolved = False
                    break
            if not all_resolved:
                break
        
        # Only change status if all conflicts are resolved
        if all_resolved:
            metadata.sync_status = SyncStatus.PENDING
        else:
            # Keep the conflict status
            metadata.sync_status = SyncStatus.CONFLICT
        
        # Update metadata in the task
        updated_task = update_nextcloud_metadata(updated_task, metadata)
        
        # Update timestamp
        updated_task["updated"] = datetime.now().timestamp()
        
        return updated_task
    
    def get_field_conflicts(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all field conflicts for a task.
        
        Args:
            task: Task to check
            
        Returns:
            List of field conflicts
        """
        conflicts = []
        
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        # Check version history for manual conflicts
        for version in metadata.version_history:
            for change in version.get("changes", []):
                if change.get("resolution") == "manual":
                    conflicts.append({
                        "field": change.get("field"),
                        "local_value": change.get("local_value"),
                        "remote_value": change.get("remote_value"),
                        "version": version.get("version")
                    })
        
        return conflicts
