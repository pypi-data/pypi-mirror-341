"""Core task management functionality for Task Blaster."""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

from rich.console import Console
from rich.prompt import Confirm
from rich.progress import Progress

from . import ai_services
from .config import TaskPriority, TaskStatus, config
from .dependency_manager import (
    get_dependent_tasks,
    update_dependent_tasks_status,
    validate_and_fix_dependencies,
    validate_task_dependencies,
)
from .ui import (
    create_loading_indicator,
    create_task_table,
    display_error,
    display_info,
    display_success,
    display_table,
    display_task_details,
)
from .utils import (
    ensure_task_structure,
    find_task_by_id,
    log,
    read_json,
    validate_task_id,
    write_json,
)


class TaskManager:
    """Main task management class."""
    
    def __init__(self, tasks_dir: Union[str, Path] = None, display_output: bool = True):
        """Initialize TaskManager.
        
        Args:
            tasks_dir: Directory to store tasks in
            display_output: Whether to display output to console (for CLI usage)
        """
        self.tasks_dir = Path(tasks_dir) if tasks_dir else config.tasks_dir
        self.tasks_file = self.tasks_dir / "tasks.json"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.display_output = display_output
    
    def _ensure_subtask_structure(self, subtask: Dict) -> Dict:
        """Ensure a subtask has all required fields with defaults."""
        defaults = {
            'status': TaskStatus.PENDING,
            'priority': TaskPriority.MEDIUM,
            'dependencies': [],
            'description': '',
            'details': ''
        }
        return {**defaults, **subtask}
    
    async def parse_prd(
        self,
        prd_path: Union[str, Path],
        num_tasks: int = 10
    ) -> Dict:
        """Parse a PRD file and generate tasks.
        
        Returns:
            Dict containing the generated tasks data
        """
        prd_path = Path(prd_path)
        if not prd_path.exists():
            raise FileNotFoundError(f"PRD file not found: {prd_path}")
        
        try:
            log.info(f"Parsing PRD file: {prd_path}")
            content = prd_path.read_text(encoding='utf-8')
            
            # Generate tasks using Claude
            tasks_data = await ai_services.call_claude(content, prd_path, num_tasks)
            
            # Ensure tasks directory exists
            self.tasks_dir.mkdir(parents=True, exist_ok=True)
            
            # Ensure task structure
            tasks_data['tasks'] = [
                ensure_task_structure(task) for task in tasks_data['tasks']
            ]
            
            # Write tasks to file
            write_json(self.tasks_file, tasks_data)
            
            log.info(f"Generated {len(tasks_data['tasks'])} tasks from PRD")
            
            # Generate individual task files
            await self.generate_task_files()
            
            if self.display_output:
                display_success(
                    f"Successfully generated {len(tasks_data['tasks'])} tasks from PRD\n\n"
                    "Next Steps:\n"
                    "1. Run 'taskinator list' to view all tasks\n"
                    "2. Run 'taskinator expand --id=<id>' to break down a task into subtasks"
                )
            
            return tasks_data
            
        except Exception as e:
            log.error(f"Error parsing PRD: {e}")
            if self.display_output:
                display_error(f"Failed to parse PRD: {e}")
            raise
    
    async def generate_task_files(self) -> List[Path]:
        """Generate individual task files from tasks.json.
        
        Returns:
            List of paths to the generated task files
        """
        try:
            log.info(f"Reading tasks from {self.tasks_file}")
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")
            
            # Validate and fix dependencies
            log.info("Validating dependencies...")
            _, _, data['tasks'] = validate_and_fix_dependencies(data['tasks'], auto_fix=True)
            
            generated_files = []
            # Generate task files
            for task in data['tasks']:
                task_path = self.tasks_dir / f"task_{str(task['id']).zfill(3)}.txt"
                content = self._format_task_file_content(task, data['tasks'])
                task_path.write_text(content, encoding='utf-8')
                log.info(f"Generated: {task_path.name}")
                generated_files.append(task_path)
            
            log.info(f"Generated {len(data['tasks'])} task files")
            return generated_files
            
        except Exception as e:
            log.error(f"Error generating task files: {e}")
            if self.display_output:
                display_error(f"Failed to generate task files: {e}")
            raise
    
    def _format_task_file_content(self, task: Dict, all_tasks: List[Dict]) -> str:
        """Format task content for file output."""
        lines = [
            f"# Task ID: {task['id']}",
            f"# Title: {task['title']}",
            f"# Status: {task['status']}",
        ]
        
        # Format dependencies
        deps = task.get('dependencies', [])
        if deps:
            dep_strings = []
            for dep_id in deps:
                dep_task = find_task_by_id(all_tasks, dep_id)
                if dep_task:
                    dep_strings.append(f"{dep_id} ({dep_task['status']})")
                else:
                    dep_strings.append(str(dep_id))
            lines.append(f"# Dependencies: {', '.join(dep_strings)}")
        else:
            lines.append("# Dependencies: None")
        
        lines.extend([
            f"# Priority: {task.get('priority', TaskPriority.MEDIUM)}",
            f"# Description: {task.get('description', '')}",
            "",
            "# Details:",
            task.get('details', ''),
            "",
            "# Test Strategy:",
            task.get('testStrategy', ''),
        ])
        
        # Add subtasks if present
        if task.get('subtasks'):
            lines.extend([
                "",
                "# Subtasks:"
            ])
            
            for subtask in task['subtasks']:
                subtask = self._ensure_subtask_structure(subtask)
                lines.extend([
                    f"## {subtask['id']}. {subtask['title']} [{subtask['status']}]"
                ])
                
                # Format subtask dependencies
                subtask_deps = subtask.get('dependencies', [])
                if subtask_deps:
                    dep_strings = []
                    for dep_id in subtask_deps:
                        if isinstance(dep_id, int):
                            dep_strings.append(f"{task['id']}.{dep_id}")
                        else:
                            dep_strings.append(str(dep_id))
                    lines.append(f"### Dependencies: {', '.join(dep_strings)}")
                else:
                    lines.append("### Dependencies: None")
                
                lines.extend([
                    f"### Priority: {subtask.get('priority', TaskPriority.MEDIUM)}",
                    f"### Description: {subtask.get('description', '')}",
                    "### Details:",
                    subtask.get('details', ''),
                    ""
                ])
        
        return "\n".join(lines)
    
    def list_tasks(self, status=None, priority=None):
        """List all tasks."""
        data = read_json(self.tasks_file)
        
        if not data or 'tasks' not in data:
            log.warning(f"No tasks found in {self.tasks_file}")
            return []
        
        tasks = data['tasks']
        
        # Filter by status if provided
        if status:
            tasks = [task for task in tasks if task.get('status') == status]
        
        # Filter by priority if provided
        if priority:
            tasks = [task for task in tasks if task.get('priority') == priority]
        
        return tasks
    
    async def expand_task(
        self,
        task_id: Union[str, int],
        num_subtasks: int = 5,
        use_research: bool = False,
        additional_context: str = "",
        display_output: Optional[bool] = None
    ) -> Dict:
        """Expand a task into subtasks.
        
        Returns:
            The updated task with subtasks
        """
        try:
            task_id = validate_task_id(task_id)
            
            log.info(f"Expanding task {task_id} into {num_subtasks} subtasks")
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")
            
            task = find_task_by_id(data['tasks'], task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            # Generate subtasks using AI
            with create_loading_indicator("Generating subtasks...") as progress:
                progress_id = progress.add_task("Generating subtasks...", total=None)
                
                subtasks = await ai_services.generate_subtasks(
                    task, num_subtasks, use_research, additional_context, progress
                )
                
                progress.update(progress_id, completed=True)
            
            # Ensure subtask structure
            subtasks = [self._ensure_subtask_structure(st) for st in subtasks]
            
            # Update task with subtasks
            task['subtasks'] = subtasks
            
            # Write updated tasks
            write_json(self.tasks_file, data)
            
            # Regenerate task files
            await self.generate_task_files()
            
            # Determine whether to display output
            should_display = self.display_output if display_output is None else display_output
            
            if should_display:
                display_success(f"Successfully expanded task {task_id} into {len(subtasks)} subtasks")
                display_task_details(task)
            
            return task
            
        except Exception as e:
            log.error(f"Error expanding task: {e}")
            # Determine whether to display output
            should_display = self.display_output if display_output is None else display_output
            if should_display:
                display_error(f"Failed to expand task: {e}")
            raise
    
    async def set_task_status(
        self,
        task_ids: Union[str, List[str]],
        new_status: str
    ) -> List[Dict]:
        """Set the status of one or more tasks.
        
        Returns:
            List of updated tasks
        """
        try:
            if not TaskStatus.is_valid(new_status):
                raise ValueError(f"Invalid status: {new_status}")
            
            # Convert string of comma-separated IDs to list if needed
            if isinstance(task_ids, str):
                task_ids = [tid.strip() for tid in task_ids.split(',')]
            
            # Validate all task IDs
            task_ids = [validate_task_id(tid) for tid in task_ids]
            
            log.info(f"Setting status of tasks {task_ids} to {new_status}")
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data:

                raise ValueError(f"No valid tasks found in {self.tasks_file}")

            # Find all tasks to update
            updated_tasks = []
            for task_id in task_ids:
                # Check if it's a subtask ID (format: parent.subtask)
                if '.' in str(task_id):
                    parent_id, subtask_id = str(task_id).split('.')
                    parent_id = int(parent_id)
                    subtask_id = int(subtask_id)
                    
                    parent = find_task_by_id(data['tasks'], parent_id)
                    if not parent or 'subtasks' not in parent:
                        raise ValueError(f"Parent task {parent_id} not found or has no subtasks")
                    
                    for subtask in parent['subtasks']:
                        if subtask['id'] == subtask_id:
                            subtask['status'] = new_status
                            updated_tasks.append(subtask)
                            break
                    else:
                        raise ValueError(f"Subtask {subtask_id} not found in task {parent_id}")
                else:
                    # Regular task
                    task = find_task_by_id(data['tasks'], task_id)
                    if not task:
                        raise ValueError(f"Task {task_id} not found")
                    
                    task['status'] = new_status
                    updated_tasks.append(task)
                    
                    # Update dependent tasks if needed
                    update_dependent_tasks_status(task_id, data['tasks'], new_status)
            
            # Write updated tasks
            write_json(self.tasks_file, data)
            
            # Regenerate task files
            await self.generate_task_files()
            
            if self.display_output:
                display_success(f"Successfully updated status of {len(updated_tasks)} tasks to {new_status}")
            
            return updated_tasks
            
        except Exception as e:
            log.error(f"Error setting task status: {e}")
            if self.display_output:
                display_error(f"Failed to set task status: {e}")
            raise
    
    async def analyze_task_complexity(
        self,
        output_file: Optional[str] = None,
        output_path: Optional[Union[str, Path]] = None,
        model_override: Optional[str] = None,
        threshold_score: float = 5.0,
        use_research: bool = False
    ) -> Dict:
        """Analyze task complexity and generate expansion recommendations.
        
        Args:
            output_file: Path to save the complexity report (alternative to output_path)
            output_path: Path to save the complexity report (deprecated)
            model_override: Override the default AI model
            threshold_score: Complexity score threshold (1-10)
            use_research: Whether to use research for analysis
        
        Returns:
            Dictionary with analysis results
        """
        try:
            # Handle both output_file and output_path for backward compatibility
            if output_file and not output_path:
                output_path = output_file
                
            output_path = Path(output_path) if output_path else self.tasks_dir / "task-complexity-report.json"
            
            log.info("Analyzing task complexity and generating expansion recommendations...")
            
            # Read tasks.json
            log.info(f"Reading tasks from {self.tasks_file}")
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data or not data['tasks']:
                raise ValueError("No tasks found in the tasks file")
            
            log.info(f"Found {len(data['tasks'])} tasks to analyze.")
            
            # Generate the prompt for AI analysis
            prompt = ai_services.generate_complexity_analysis_prompt(data)
            
            # Start loading indicator
            loading = create_loading_indicator(
                "Analyzing task complexity..." if not use_research else 
                "Analyzing task complexity with research..."
            )
            
            try:
                # Get complexity analysis from AI
                complexity_analysis = await ai_services.analyze_task_complexity(
                    data['tasks'],
                    prompt,
                    use_research,
                    model_override
                )
                
                # Check for missing task analysis
                task_ids = {task['id'] for task in data['tasks']}
                analysis_ids = {analysis['taskId'] for analysis in complexity_analysis}
                missing_ids = task_ids - analysis_ids
                
                if missing_ids:
                    log.warning(f"Missing analysis for tasks: {missing_ids}")
                    
                    # Create subset of missing tasks
                    missing_tasks = {
                        'meta': data.get('meta', {}),
                        'tasks': [t for t in data['tasks'] if t['id'] in missing_ids]
                    }
                    
                    # Generate prompt for missing tasks
                    missing_prompt = ai_services.generate_complexity_analysis_prompt(missing_tasks)
                    
                    # Analyze missing tasks
                    missing_analysis = await ai_services.analyze_task_complexity(
                        missing_tasks['tasks'],
                        missing_prompt,
                        use_research,
                        model_override
                    )
                    
                    # Add missing analysis to main results
                    complexity_analysis.extend(missing_analysis)
                
                # Create the final report
                report = {
                    'meta': {
                        'generatedAt': datetime.now().isoformat(),
                        'tasksAnalyzed': len(data['tasks']),
                        'thresholdScore': threshold_score,
                        'projectName': data.get('meta', {}).get('projectName', 'Your Project Name'),
                        'usedResearch': use_research
                    },
                    'complexityAnalysis': complexity_analysis
                }
                
                # Write the report
                log.info(f"Writing complexity report to {output_path}")
                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                write_json(output_path, report)
                
                # Display summary
                high_complexity = sum(1 for t in complexity_analysis if t['complexityScore'] >= 8)
                medium_complexity = sum(1 for t in complexity_analysis if 5 <= t['complexityScore'] < 8)
                low_complexity = sum(1 for t in complexity_analysis if t['complexityScore'] < 5)
                total_analyzed = len(complexity_analysis)
                
                if self.display_output:
                    console = Console()
                    console.print()
                    console.print("[bold]Complexity Analysis Summary:[/bold]")
                    console.print("----------------------------")
                    console.print(f"Tasks in input file: {len(data['tasks'])}")
                    console.print(f"Tasks successfully analyzed: {total_analyzed}")
                    console.print(f"High complexity tasks: [bold red]{high_complexity}[/bold red]")
                    console.print(f"Medium complexity tasks: [bold yellow]{medium_complexity}[/bold yellow]")
                    console.print(f"Low complexity tasks: [bold green]{low_complexity}[/bold green]")
                    console.print(f"Sum verification: {high_complexity + medium_complexity + low_complexity} (should equal {total_analyzed})")
                    console.print(f"Research-backed analysis: {'Yes' if use_research else 'No'}")
                    console.print()
                    console.print(f"See [cyan]{output_path}[/cyan] for the full report and expansion commands.")
                    console.print()
                    
                    display_success("Task complexity analysis complete")
                
            finally:
                loading.stop()
                
            return report
            
        except Exception as e:
            log.error(f"Error analyzing task complexity: {e}")
            if self.display_output:
                display_error(f"Failed to analyze task complexity: {e}")
            raise
    
    def show_next_task(self) -> Optional[Dict]:
        """Show the next task to work on based on priority and dependencies.
        
        Returns:
            The next task to work on, or None if no eligible tasks
        """
        try:
            data = read_json(self.tasks_file)
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")

            # Get completed task IDs
            completed_task_ids = {
                task['id'] for task in data['tasks']
                if task['status'] == TaskStatus.DONE
            }

            # Filter for eligible tasks (pending/in-progress with satisfied dependencies)
            eligible_tasks = [
                task for task in data['tasks']
                if (task['status'] in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS) and
                    all(dep_id in completed_task_ids for dep_id in task.get('dependencies', [])))
            ]

            if not eligible_tasks:
                if self.display_output:
                    display_info("No eligible tasks found. All tasks are either completed or blocked by dependencies.")
                return None

            # Sort by priority, dependency count, and ID
            priority_values = {
                TaskPriority.HIGH: 3,
                TaskPriority.MEDIUM: 2,
                TaskPriority.LOW: 1
            }

            def task_sort_key(task: Dict) -> Tuple[int, int, int]:
                priority = priority_values.get(task.get('priority', TaskPriority.MEDIUM), 2)
                dep_count = len(task.get('dependencies', []))
                return (-priority, dep_count, task['id'])

            next_task = min(eligible_tasks, key=task_sort_key)
            
            if self.display_output:
                display_info("Next task to work on:")
                display_task_details(next_task)
                
            return next_task

        except Exception as e:
            log.error(f"Error showing next task: {e}")
            if self.display_output:
                display_error(f"Failed to show next task: {e}")
            raise
    
    def show_task(self, task_id: Union[str, int]) -> Optional[Dict]:
        """Show detailed information about a specific task.
        
        Returns:
            The task details, or None if not found
        """
        try:
            task_id = validate_task_id(task_id)
            
            data = read_json(self.tasks_file)
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")
            
            task = find_task_by_id(data['tasks'], task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            if self.display_output:
                display_task_details(task)
            
            return task
            
        except Exception as e:
            log.error(f"Error showing task: {e}")
            if self.display_output:
                display_error(f"Failed to show task: {e}")
            raise
    
    async def add_task(
        self,
        prompt: str,
        dependencies: List[int] = None,
        priority: str = "medium"
    ) -> Dict:
        """Add a new task using AI.
        
        Args:
            prompt: Description of the task to add
            dependencies: List of task IDs this task depends on
            priority: Task priority (high, medium, low)
            
        Returns:
            The newly created task
        """
        try:
            log.info(f"Adding new task: {prompt}")
            
            # Read existing tasks
            data = read_json(self.tasks_file)
            if not data:
                data = {"tasks": []}
            
            # Generate task details using AI
            task_details = await ai_services.generate_task_details(prompt)
            
            # Create new task
            new_task = {
                "id": len(data["tasks"]) + 1,
                "title": task_details["title"],
                "description": task_details["description"],
                "details": task_details["details"],
                "testStrategy": task_details["testStrategy"],
                "dependencies": dependencies or [],
                "priority": priority,
                "status": TaskStatus.PENDING
            }
            
            # Add task to list
            data["tasks"].append(new_task)
            
            # Write updated tasks
            write_json(self.tasks_file, data)
            
            # Regenerate task files
            await self.generate_task_files()
            
            if self.display_output:
                display_success(f"Successfully added task {new_task['id']}")
                display_task_details(new_task)
            
            return new_task
            
        except Exception as e:
            log.error(f"Error adding task: {e}")
            if self.display_output:
                display_error(f"Failed to add task: {e}")
            raise
    
    def review_complexity_recommendations(
        self,
        report_file: str = "tasks/task-complexity-report.json",
        threshold: float = 5.0,
        non_interactive: bool = False
    ) -> List[Dict[str, Any]]:
        """Review task complexity recommendations and approve tasks for expansion.
        
        Args:
            report_file: Path to the complexity report file
            threshold: Complexity score threshold for recommending expansion
            non_interactive: If True, approve all recommendations above threshold
            
        Returns:
            List of approved task expansions
        """
        try:
            # Read the complexity report
            if not os.path.exists(report_file):
                raise ValueError(f"Complexity report file not found: {report_file}")
            
            with open(report_file, "r") as f:
                report = json.load(f)
            
            if "complexityAnalysis" not in report:
                raise ValueError(f"Invalid complexity report format in {report_file}")
            
            # Filter tasks above threshold
            tasks_to_review = [
                task for task in report["complexityAnalysis"]
                if task.get("complexityScore", 0) >= threshold and task.get("recommendedSubtasks", 0) > 0
            ]
            
            if not tasks_to_review:
                if self.display_output:
                    display_info(f"No tasks found with complexity score >= {threshold}")
                return []
            
            approved_tasks = []
            
            # In non-interactive mode, approve all tasks above threshold
            if non_interactive:
                approved_tasks = tasks_to_review
                if self.display_output:
                    display_info(f"Auto-approved {len(approved_tasks)} tasks for expansion")
                return approved_tasks
            
            # Interactive review
            if self.display_output:
                from rich.panel import Panel
                from rich.text import Text
                from rich.columns import Columns
                from rich.padding import Padding
                
                console = Console()
                
                # Display header
                console.print()
                display_info(f"Found {len(tasks_to_review)} tasks with complexity score >= {threshold}")
                console.print(Panel(
                    "[bold]Review each task and approve for expansion[/bold]",
                    border_style="blue",
                    expand=False
                ))
                console.print()
                
                for task in tasks_to_review:
                    task_id = task.get("taskId")
                    title = task.get("taskTitle", "Unknown")
                    score = task.get("complexityScore", 0)
                    subtasks = task.get("recommendedSubtasks", 0)
                    prompt = task.get("expansionPrompt", "")
                    reasoning = task.get("reasoning", "")
                    
                    # Create score indicator with color based on complexity
                    score_color = "green" if score < 6 else "yellow" if score < 8 else "red"
                    score_text = Text(f"{score}/10", style=f"bold {score_color}")
                    
                    # Create task header
                    task_header = Panel(
                        f"[bold cyan]Task {task_id}:[/bold cyan] [bold]{title}[/bold]",
                        border_style="cyan",
                        expand=False
                    )
                    
                    # Create complexity panel
                    complexity_panel = Panel(
                        Columns([
                            f"[bold]Complexity:[/bold] {score_text}",
                            f"[bold]Subtasks:[/bold] {subtasks}"
                        ]),
                        title="Complexity",
                        border_style="blue",
                        expand=False
                    )
                    
                    # Create reasoning panel
                    reasoning_panel = Panel(
                        Text(reasoning, justify="left"),
                        title="Reasoning",
                        border_style="blue",
                        expand=False
                    )
                    
                    # Create expansion prompt panel
                    prompt_panel = Panel(
                        Text(prompt, justify="left"),
                        title="Expansion Prompt",
                        border_style="green",
                        expand=False
                    )
                    
                    # Display all panels
                    console.print(task_header)
                    console.print(complexity_panel)
                    console.print(reasoning_panel)
                    console.print(prompt_panel)
                    
                    # Ask for approval with better formatting
                    console.print()
                    approve = Confirm.ask("[bold]Approve this task for expansion?[/bold]")
                    if approve:
                        approved_tasks.append(task)
                        console.print("[bold green]✓ Task approved for expansion[/bold green]")
                    else:
                        console.print("[bold yellow]✗ Task skipped[/bold yellow]")
                    
                    # Add separator between tasks
                    console.print("\n" + "─" * 80 + "\n")
            
            return approved_tasks
            
        except Exception as e:
            log.error(f"Error reviewing recommendations: {e}")
            if self.display_output:
                display_error(f"Failed to review recommendations: {e}")
            raise
    
    async def sync_tasks(
        self,
        system: Optional[str] = None,
        task_id: Optional[Union[str, int]] = None,
        direction: str = "bidirectional",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Synchronize tasks with external systems.
        
        Args:
            system: External system to sync with (if None, sync with all configured systems)
            task_id: ID of the task to sync (if None, sync all tasks)
            direction: Synchronization direction ('local_to_remote', 'remote_to_local', 'bidirectional')
            config: Configuration for external systems
            
        Returns:
            Synchronization results
        """
        try:
            from .sync_manager import SyncManager
            from .external_integration import ExternalSystem, SyncDirection
            
            # Validate direction
            if direction not in (SyncDirection.LOCAL_TO_REMOTE, SyncDirection.REMOTE_TO_LOCAL, SyncDirection.BIDIRECTIONAL):
                direction = SyncDirection.BIDIRECTIONAL
            
            # Initialize config if not provided
            if config is None:
                config = {}
            
            # Get credentials from environment if not in config
            import os
            
            # NextCloud credentials
            if "nextcloud" not in config:
                config["nextcloud"] = {
                    "host": os.getenv("NEXTCLOUD_HOST"),
                    "username": os.getenv("NEXTCLOUD_USERNAME"),
                    "password": os.getenv("NEXTCLOUD_PASSWORD"),
                    "token": os.getenv("NEXTCLOUD_TOKEN")
                }
            
            # Initialize sync manager
            sync_manager = SyncManager(
                tasks_file=self.tasks_file,
                nextcloud_host=config.get("nextcloud", {}).get("host"),
                nextcloud_username=config.get("nextcloud", {}).get("username"),
                nextcloud_password=config.get("nextcloud", {}).get("password"),
                nextcloud_token=config.get("nextcloud", {}).get("token")
            )
            
            # Sync tasks
            if task_id:
                # Validate task ID
                from .utils import validate_task_id
                task_id = validate_task_id(task_id)
                
                # Sync specific task
                result = await sync_manager.sync_task(task_id, direction)
            else:
                # Sync all tasks
                result = await sync_manager.sync_all(direction)
            
            # Display results if needed
            if self.display_output:
                from rich.console import Console
                from rich.table import Table
                
                console = Console()
                console.print()
                console.print("[bold]Synchronization Results:[/bold]")
                console.print("------------------------")
                
                if "status" in result:
                    status_color = "green" if result["status"] == "success" else "red"
                    console.print(f"Status: [{status_color}]{result['status']}[/{status_color}]")
                
                if "message" in result:
                    console.print(f"Message: {result['message']}")
                
                if "total" in result:
                    console.print(f"Total tasks: {result['total']}")
                    console.print(f"Synced: {result['synced']}")
                    console.print(f"Errors: {result['errors']}")
                    console.print(f"Conflicts: {result['conflicts']}")
                    console.print(f"Skipped: {result['skipped']}")
                
                if "details" in result and result["details"]:
                    console.print()
                    console.print("[bold]Details:[/bold]")
                    
                    table = Table(show_header=True)
                    table.add_column("Task ID")
                    table.add_column("System")
                    table.add_column("Status")
                    table.add_column("Message")
                    
                    for detail in result["details"]:
                        status = detail.get("status", "")
                        status_color = "green" if status == "success" else "red" if status == "error" else "yellow"
                        
                        table.add_row(
                            str(detail.get("task_id", "")),
                            detail.get("system", ""),
                            f"[{status_color}]{status}[/{status_color}]",
                            detail.get("message", "")
                        )
                    
                    console.print(table)
            
            return result
            
        except Exception as e:
            log.error(f"Error syncing tasks: {e}")
            if self.display_output:
                display_error(f"Failed to sync tasks: {e}")
            raise
    
    async def resolve_conflict(
        self,
        task_id: Union[str, int],
        system: str,
        resolution: str = "local",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Resolve a synchronization conflict.
        
        Args:
            task_id: ID of the task with conflict
            system: External system identifier
            resolution: Conflict resolution strategy ('local', 'remote', or 'merge')
            config: Configuration for external systems
            
        Returns:
            Resolution results
        """
        try:
            from .sync_manager import SyncManager
            
            # Validate task ID
            from .utils import validate_task_id
            task_id = validate_task_id(task_id)
            
            # Initialize config if not provided
            if config is None:
                config = {}
            
            # Get credentials from environment if not in config
            import os
            
            # NextCloud credentials
            if "nextcloud" not in config:
                config["nextcloud"] = {
                    "host": os.getenv("NEXTCLOUD_HOST"),
                    "username": os.getenv("NEXTCLOUD_USERNAME"),
                    "password": os.getenv("NEXTCLOUD_PASSWORD"),
                    "token": os.getenv("NEXTCLOUD_TOKEN")
                }
            
            # Initialize sync manager
            sync_manager = SyncManager(
                tasks_file=self.tasks_file,
                nextcloud_host=config.get("nextcloud", {}).get("host"),
                nextcloud_username=config.get("nextcloud", {}).get("username"),
                nextcloud_password=config.get("nextcloud", {}).get("password"),
                nextcloud_token=config.get("nextcloud", {}).get("token")
            )
            
            # Resolve conflict
            result = await sync_manager.resolve_conflict(task_id, system, resolution)
            
            # Display results if needed
            if self.display_output:
                from rich.console import Console
                
                console = Console()
                console.print()
                console.print("[bold]Conflict Resolution Results:[/bold]")
                console.print("-----------------------------")
                
                status_color = "green" if result["status"] == "success" else "red"
                console.print(f"Status: [{status_color}]{result['status']}[/{status_color}]")
                
                if "message" in result:
                    console.print(f"Message: {result['message']}")
            
            return result
            
        except Exception as e:
            log.error(f"Error resolving conflict: {e}")
            if self.display_output:
                display_error(f"Failed to resolve conflict: {e}")
            raise