"""Command-line interface for Task Blaster."""

import asyncio
import functools
import importlib
import importlib.resources
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__, package_data
from .config import TaskStatus, config
from .external_integration.sync_metadata_store import SyncMetadataStore
from .sync_manager import SyncManager
from .task_manager import TaskManager
from .ui import display_banner, display_error, display_info, display_success, display_table
from .utils import log, find_task_by_id, read_json, write_json

# Create Typer app
app = typer.Typer(
    help="Task Blaster: AI-powered task management for developers",
    add_completion=False
)

# Wrapper for async commands
def _run_async(func):
    """Decorator to run async functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper

def get_task_manager(display_output: bool = True) -> TaskManager:
    """Get a TaskManager instance."""
    return TaskManager(display_output=display_output)

@app.command()
def version():
    """Show the version of Task Blaster."""
    console = Console()
    console.print(f"Task Blaster v{__version__}")

@app.command()
def init(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force initialization even if files exist"
    )
):
    """Initialize a new Task Blaster project."""
    try:
        # Create directories
        Path("tasks").mkdir(exist_ok=True)
        
        # Create cursor and windsurf metadata directories
        cursor_rules_dir = Path(".cursor/rules")
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        display_info(f"Created directory: {cursor_rules_dir}")
        
        # Create windsurf directory
        windsurf_dir = Path(".windsurf")
        windsurf_dir.mkdir(parents=True, exist_ok=True)
        display_info(f"Created directory: {windsurf_dir}")
        
        # Copy windsurf rules template
        windsurf_rules_file = Path(".windsurfrules")
        
        if not windsurf_rules_file.exists() or force:
            # Get the template content from package data
            template_path = Path(__file__).parent / "package_data" / "templates" / "windsurf" / ".windsurfrules"
            if template_path.exists():
                with open(template_path, 'r') as src:
                    with open(windsurf_rules_file, 'w') as dst:
                        dst.write(src.read())
                display_info(f"Created file: {windsurf_rules_file}")
            else:
                display_info(f"Template file not found: {template_path}")
        
        # Create tasks.json if it doesn't exist or force is True
        tasks_file = Path("tasks/tasks.json")
        if not tasks_file.exists() or force:
            tasks_data = {
                "tasks": []
            }
            with open(tasks_file, "w") as f:
                json.dump(tasks_data, f, indent=2)
            
            display_success("Initialized Task Blaster project")
        else:
            display_error("Task Blaster project already initialized. Use --force to reinitialize.")
            raise typer.Exit(1)
    
    except Exception as e:
        log.error(f"Error initializing project: {e}")
        display_error(f"Failed to initialize project: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def parse_prd(
    prd_file: str = typer.Argument(..., help="Path to the PRD file"),
    num_tasks: int = typer.Option(
        None, "--num-tasks", "-n", help="Number of tasks to generate"
    )
):
    """Parse a PRD file and generate tasks."""
    try:
        task_manager = get_task_manager()
        await task_manager.parse_prd(prd_file, num_tasks)
    except Exception as e:
        display_error(f"Failed to parse PRD: {e}")
        raise typer.Exit(1)

@app.command()
def list(
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status"
    ),
    priority: Optional[str] = typer.Option(
        None, "--priority", "-p", help="Filter by priority"
    )
):
    """List all tasks."""
    try:
        task_manager = get_task_manager()
        tasks = task_manager.list_tasks(status=status, priority=priority)
        display_task_list(tasks)
    except Exception as e:
        display_error(f"Failed to list tasks: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def expand_task(
    task_id: str = typer.Argument(..., help="ID of the task to expand"),
    num_subtasks: int = typer.Option(
        5, "--num-subtasks", "-n", help="Number of subtasks to generate"
    ),
    use_research: bool = typer.Option(
        False, "--research", "-r", help="Use research for generating subtasks"
    ),
    additional_context: str = typer.Option(
        "", "--context", "-c", help="Additional context for generating subtasks"
    )
):
    """Expand a task into subtasks."""
    try:
        display_banner()
        task_manager = get_task_manager()
        await task_manager.expand_task(
            task_id,
            num_subtasks,
            use_research,
            additional_context
        )
    except Exception as e:
        display_error(f"Failed to expand task: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def status(
    task_id: str = typer.Argument(..., help="ID of the task to update"),
    status: str = typer.Argument(..., help="New status for the task")
):
    """Set the status of one or more tasks."""
    try:
        task_manager = get_task_manager()
        await task_manager.set_task_status(task_id, status)
    except Exception as e:
        display_error(f"Failed to update task status: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def analyze(
    output_file: str = typer.Option(
        "tasks/task-complexity-report.json", 
        "--output", 
        "-o", 
        help="Path to save the complexity report"
    ),
    use_research: bool = typer.Option(
        False, 
        "--research", 
        "-r", 
        help="Use research for analysis"
    )
):
    """Analyze task complexity and generate expansion recommendations."""
    try:
        task_manager = get_task_manager()
        await task_manager.analyze_task_complexity(
            output_file=output_file,
            use_research=use_research
        )
    except Exception as e:
        display_error(f"Failed to analyze tasks: {e}")
        raise typer.Exit(1)

@app.command()
def next():
    """Show the next task to work on."""
    try:
        task_manager = get_task_manager()
        task_manager.show_next_task()
    except Exception as e:
        display_error(f"Failed to show next task: {e}")
        raise typer.Exit(1)

@app.command()
def show(
    task_id: str = typer.Argument(..., help="ID of the task to show")
):
    """Show detailed information about a task."""
    try:
        task_manager = get_task_manager()
        task_manager.show_task(task_id)
    except Exception as e:
        display_error(f"Failed to show task: {e}")
        raise typer.Exit(1)

@app.command()
def review(
    report_file: str = typer.Option(
        "tasks/task-complexity-report.json", 
        "--report", 
        "-r", 
        help="Path to the complexity report file"
    ),
    threshold: float = typer.Option(
        5.0, 
        "--threshold", 
        "-t", 
        help="Complexity score threshold for recommending expansion"
    ),
    output_file: str = typer.Option(
        "tasks/approved-expansions.json", 
        "--output", 
        "-o", 
        help="Path to save the approved expansions"
    ),
    non_interactive: bool = typer.Option(
        False, 
        "--non-interactive", 
        "-n", 
        help="Run in non-interactive mode, approving all recommendations above threshold"
    )
):
    """Review task complexity recommendations and approve tasks for expansion."""
    try:
        task_manager = get_task_manager()
        approved_tasks = task_manager.review_complexity_recommendations(
            report_file=report_file,
            threshold=threshold,
            non_interactive=non_interactive
        )
        
        # Save approved tasks to file
        if approved_tasks:
            with open(output_file, "w") as f:
                json.dump({"approved_expansions": approved_tasks}, f, indent=2)
            
            if task_manager.display_output:
                display_success(f"Saved {len(approved_tasks)} approved expansions to {output_file}")
                display_info("Run 'taskinator implement' to expand these tasks")
        else:
            if task_manager.display_output:
                display_info("No tasks were approved for expansion")
    
    except Exception as e:
        log.error(f"Error reviewing recommendations: {e}")
        if task_manager.display_output:
            display_error(f"Failed to review recommendations: {e}")

@app.command()
@_run_async
async def implement(
    approved_file: str = typer.Option(
        "tasks/approved-expansions.json", 
        "--approved", 
        "-a", 
        help="Path to the approved expansions file"
    ),
    num_subtasks: int = typer.Option(
        None, 
        "--num-subtasks", 
        "-n", 
        help="Override the recommended number of subtasks"
    )
):
    """Implement approved task expansions by expanding tasks into subtasks."""
    try:
        task_manager = get_task_manager()
        
        # Read the approved expansions file
        if not Path(approved_file).exists():
            if task_manager.display_output:
                display_error(f"Approved expansions file not found: {approved_file}")
            raise typer.Exit(1)
        
        with open(approved_file, "r") as f:
            approved_data = json.load(f)
        
        if "approved_expansions" not in approved_data or not approved_data["approved_expansions"]:
            if task_manager.display_output:
                display_error("No approved expansions found in the file")
            raise typer.Exit(1)
        
        approved_expansions = approved_data["approved_expansions"]
        
        # Display banner
        display_banner()
        
        # Show summary of what will be implemented
        console = Console()
        console.print()
        
        # Create a table showing tasks to be expanded
        table = Table(title="Tasks to be Expanded", show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Task", style="white")
        table.add_column("Subtasks", justify="center")
        
        for expansion in approved_expansions:
            task_id = expansion.get("taskId")
            title = expansion.get("taskTitle", "Unknown")
            subtask_count = num_subtasks if num_subtasks is not None else expansion.get("recommendedSubtasks", 5)
            table.add_row(
                str(task_id),
                title,
                str(subtask_count)
            )
        
        console.print(Panel(table, border_style="blue", expand=False))
        console.print()
        
        # Process each approved expansion
        successful_expansions = 0
        
        for i, expansion in enumerate(approved_expansions):
            task_id = expansion.get("taskId")
            if not task_id:
                continue
                
            # Get the recommended number of subtasks or use the override
            subtask_count = num_subtasks if num_subtasks is not None else expansion.get("recommendedSubtasks", 5)
            
            # Get the expansion prompt
            expansion_prompt = expansion.get("expansionPrompt", "")
            
            # Show progress
            progress_text = f"[{i+1}/{len(approved_expansions)}] "
            console.print(f"{progress_text}[bold cyan]Expanding Task {task_id}[/bold cyan]: {expansion.get('taskTitle', '')}")
            
            try:
                # Expand the task
                expanded_task = await task_manager.expand_task(
                    task_id=task_id,
                    num_subtasks=subtask_count,
                    additional_context=expansion_prompt,
                    display_output=False  # We'll handle our own output
                )
                
                # Show success message
                console.print(f"{' ' * len(progress_text)}[bold green]✓[/bold green] Successfully expanded into {len(expanded_task.get('subtasks', []))} subtasks")
                successful_expansions += 1
                
            except Exception as e:
                # Show error message
                console.print(f"{' ' * len(progress_text)}[bold red]✗[/bold red] Failed: {str(e)}")
            
            # Add separator between tasks
            if i < len(approved_expansions) - 1:
                console.print()
        
        # Show final summary
        console.print()
        if successful_expansions == len(approved_expansions):
            display_success(f"Successfully implemented all {successful_expansions} task expansions")
        else:
            display_info(f"Implemented {successful_expansions} out of {len(approved_expansions)} task expansions")
        
        # Suggest next steps
        console.print(Panel(
            "[bold]Next Steps:[/bold]\n"
            "1. Run [cyan]taskinator list[/cyan] to view all tasks\n"
            "2. Run [cyan]taskinator analyze[/cyan] to analyze the complexity of the new subtasks",
            title="What's Next",
            border_style="green",
            expand=False
        ))
    
    except Exception as e:
        log.error(f"Error implementing expansions: {e}")
        if task_manager.display_output:
            display_error(f"Failed to implement expansions: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def sync_tasks(
    system: str = typer.Option("nextcloud", "--system", "-s", help="External system to sync with (e.g., nextcloud)"),
    direction: str = typer.Option("bidirectional", "--direction", "-d", help="Sync direction (bidirectional, local_to_remote, remote_to_local)"),
    task_id: Optional[str] = typer.Option(None, "--task", "-t", help="Specific task ID to sync, if not provided all tasks will be synced"),
    calendar: str = typer.Option("Taskinator", "--calendar", "-c", help="Calendar name to use (for NextCloud)"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output, including credentials being used"
    ),
):
    """Synchronize tasks with external systems."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get configuration for the system
        config = get_sync_config(system)
        
        if verbose:
            display_info(f"Using credentials for {system}:")
            for key, value in config.items():
                if key in ["host", "username"]:
                    display_info(f"  {key}: {value}")
                elif key in ["password", "token"]:
                    if value:
                        display_info(f"  {key}: ***")
                    else:
                        display_info(f"  {key}: <not set>")
            display_info(f"Using calendar: {calendar}")
        
        # Get task manager
        task_manager = TaskManager()
        
        # Create sync manager
        nextcloud_config = config.get("nextcloud", {})
        sync_manager = SyncManager(
            tasks_file=task_manager.tasks_file,
            nextcloud_host=nextcloud_config.get("host"),
            nextcloud_username=nextcloud_config.get("username"),
            nextcloud_password=nextcloud_config.get("password"),
            nextcloud_token=nextcloud_config.get("token"),
            nextcloud_calendar=calendar,
            verbose=verbose
        )
        
        try:
            # Initialize the sync manager
            await sync_manager.initialize()
            
            # Parse direction
            if direction not in ["bidirectional", "local_to_remote", "remote_to_local"]:
                display_error(f"Invalid direction: {direction}. Must be one of: bidirectional, local_to_remote, remote_to_local")
                raise typer.Exit(1)
            
            # Sync tasks
            if task_id:
                # Sync specific task
                result = await sync_manager.sync_task(int(task_id), direction)
                
                # Display result
                if result["status"] == "success":
                    display_success(f"Successfully synced task {task_id}")
                else:
                    display_error(f"Error syncing task {task_id}: {result.get('message', 'Unknown error')}")
            else:
                # Sync all tasks
                result = await sync_manager.sync_all(direction)
                
                # Display results
                if result["status"] == "success":
                    display_success("Synchronization completed")
                    
                    # Create table
                    table = Table(title="Synchronization Results")
                    table.add_column("Task ID")
                    table.add_column("System")
                    table.add_column("Status")
                    table.add_column("Message")
                    
                    for detail in result.get("details", []):
                        task_id = detail.get("task_id", "")
                        system = detail.get("system", "")
                        status = detail.get("status", "")
                        message = detail.get("message", "")
                        
                        table.add_row(
                            str(task_id),
                            system,
                            status,
                            message
                        )
                    
                    # Display table
                    display_table(table)
                    
                    # Display summary
                    display_info(f"Total tasks: {result.get('total', 0)}")
                    display_info(f"Synced: {result.get('synced', 0)}")
                    display_info(f"Errors: {result.get('errors', 0)}")
                    display_info(f"Conflicts: {result.get('conflicts', 0)}")
                    display_info(f"Skipped: {result.get('skipped', 0)}")
                else:
                    display_error(f"Error syncing tasks: {result.get('message', 'Unknown error')}")
        finally:
            # Ensure we close any open sessions
            if hasattr(sync_manager, 'adapters') and system in sync_manager.adapters:
                adapter = sync_manager.adapters[system]
                if hasattr(adapter, 'client') and adapter.client:
                    if hasattr(adapter.client, 'session') and adapter.client.session:
                        await adapter.client.session.close()
                        if verbose:
                            display_info("Closed client session")
    
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def init_sync(
    system: str = typer.Option("nextcloud", "--system", "-s", help="External system to sync with (e.g., nextcloud)"),
    calendar: str = typer.Option("Taskinator", "--calendar", "-c", help="Calendar name to use (will be created if it doesn't exist)"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output, including credentials being used"
    ),
):
    """Initialize synchronization with an external system."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get configuration for the system
        config = get_sync_config(system)
        
        if verbose:
            display_info(f"Using credentials for {system}:")
            for key, value in config.items():
                if key in ["host", "username"]:
                    display_info(f"  {key}: {value}")
                elif key in ["password", "token"]:
                    if value:
                        display_info(f"  {key}: ***")
                    else:
                        display_info(f"  {key}: <not set>")
            display_info(f"Using calendar: {calendar}")
        
        # Create sync manager
        nextcloud_config = config.get("nextcloud", {})
        sync_manager = SyncManager(
            tasks_file=None,  # No need for tasks file for initialization
            nextcloud_host=nextcloud_config.get("host"),
            nextcloud_username=nextcloud_config.get("username"),
            nextcloud_password=nextcloud_config.get("password"),
            nextcloud_token=nextcloud_config.get("token"),
            nextcloud_calendar=calendar,
            verbose=verbose
        )
        
        try:
            # Initialize the sync manager
            display_info(f"Initializing synchronization with {system}...")
            results = await sync_manager.initialize()
            
            # Check if initialization was successful
            if system in results:
                if results[system]["status"] == "success":
                    display_success(f"Synchronization initialized successfully with {system}")
                    display_info(f"Calendar '{calendar}' is ready for use")
                else:
                    display_error(f"Failed to initialize synchronization with {system}: {results[system]['message']}")
                    display_info("However, you may still be able to use existing calendars if they were found.")
            else:
                display_error(f"No initialization results for {system}")
        
        finally:
            # Ensure we close any open sessions
            if hasattr(sync_manager, 'adapters') and system in sync_manager.adapters:
                adapter = sync_manager.adapters[system]
                if hasattr(adapter, 'client') and adapter.client:
                    if hasattr(adapter.client, 'session') and adapter.client.session:
                        await adapter.client.session.close()
                        if verbose:
                            display_info("Closed client session")
        
    except Exception as e:
        display_error(f"Error initializing synchronization: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def push_tasks(
    system: str = typer.Option("nextcloud", "--system", "-s", help="External system to push to (e.g., nextcloud)"),
    task_id: str = typer.Option(None, "--task-id", "-i", help="ID of the task to push (if omitted, pushes all tasks)"),
    calendar: str = typer.Option("Taskinator", "--calendar", "-c", help="Calendar name to use (will be created if it doesn't exist)"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output, including credentials being used"
    ),
):
    """Push tasks to an external system."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get task manager
        task_manager = TaskManager()
        
        # Get configuration for the system
        config = get_sync_config(system)
        
        if verbose:
            display_info(f"Using credentials for {system}:")
            for key, value in config.items():
                if key in ["host", "username"]:
                    display_info(f"  {key}: {value}")
                elif key in ["password", "token"]:
                    if value:
                        display_info(f"  {key}: ***")
                    else:
                        display_info(f"  {key}: <not set>")
            display_info(f"Using calendar: {calendar}")
        
        # Create sync manager
        nextcloud_config = config.get("nextcloud", {})
        sync_manager = SyncManager(
            tasks_file=task_manager.tasks_file,
            nextcloud_host=nextcloud_config.get("host"),
            nextcloud_username=nextcloud_config.get("username"),
            nextcloud_password=nextcloud_config.get("password"),
            nextcloud_token=nextcloud_config.get("token"),
            nextcloud_calendar=calendar,
            verbose=verbose
        )
        
        try:
            # Initialize the sync manager
            await sync_manager.initialize()
            
            # Sync tasks with direction=push
            if task_id:
                # Sync specific task
                result = await sync_manager.sync_task(int(task_id), "local_to_remote")
                
                # Display result
                if result["status"] == "success":
                    display_success(f"Successfully pushed task {task_id}")
                else:
                    display_error(f"Error pushing task {task_id}: {result.get('message', 'Unknown error')}")
            else:
                # Sync all tasks
                result = await sync_manager.sync_all("local_to_remote")
                
                # Display results
                if result["status"] == "success":
                    display_success("Push completed")
                    
                    # Create table
                    table = Table(title="Push Results")
                    table.add_column("Task ID")
                    table.add_column("System")
                    table.add_column("Status")
                    table.add_column("Message")
                    
                    for detail in result.get("details", []):
                        task_id = detail.get("task_id", "")
                        system = detail.get("system", "")
                        status = detail.get("status", "")
                        message = detail.get("message", "")
                        
                        table.add_row(
                            str(task_id),
                            system,
                            status,
                            message
                        )
                    
                    # Display table
                    display_table(table)
                    
                    # Display summary
                    display_info(f"Total tasks: {result.get('total', 0)}")
                    display_info(f"Pushed: {result.get('synced', 0)}")
                    display_info(f"Errors: {result.get('errors', 0)}")
                    display_info(f"Skipped: {result.get('skipped', 0)}")
                else:
                    display_error(f"Error pushing tasks: {result.get('message', 'Unknown error')}")
        finally:
            # Ensure we close any open sessions
            if hasattr(sync_manager, 'adapters') and system in sync_manager.adapters:
                adapter = sync_manager.adapters[system]
                if hasattr(adapter, 'client') and adapter.client:
                    if hasattr(adapter.client, 'session') and adapter.client.session:
                        await adapter.client.session.close()
                        if verbose:
                            display_info("Closed client session")
    
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def pull_tasks(
    system: str = typer.Option("nextcloud", "--system", "-s", help="External system to pull from (e.g., nextcloud)"),
    task_id: str = typer.Option(None, "--task-id", "-i", help="ID of the task to pull (if omitted, pulls all tasks)"),
    calendar: str = typer.Option("Taskinator", "--calendar", "-c", help="Calendar name to use (will be created if it doesn't exist)"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output, including credentials being used"
    ),
):
    """Pull tasks from an external system."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get task manager
        task_manager = TaskManager()
        
        # Get configuration for the system
        config = get_sync_config(system)
        
        if verbose:
            display_info(f"Using credentials for {system}:")
            for key, value in config.items():
                if key in ["host", "username"]:
                    display_info(f"  {key}: {value}")
                elif key in ["password", "token"]:
                    if value:
                        display_info(f"  {key}: ***")
                    else:
                        display_info(f"  {key}: <not set>")
            display_info(f"Using calendar: {calendar}")
        
        # Create sync manager
        nextcloud_config = config.get("nextcloud", {})
        sync_manager = SyncManager(
            tasks_file=task_manager.tasks_file,
            nextcloud_host=nextcloud_config.get("host"),
            nextcloud_username=nextcloud_config.get("username"),
            nextcloud_password=nextcloud_config.get("password"),
            nextcloud_token=nextcloud_config.get("token"),
            nextcloud_calendar=calendar,
            verbose=verbose
        )
        
        try:
            # Initialize the sync manager
            await sync_manager.initialize()
            
            # Sync tasks with direction=pull
            if task_id:
                # Sync specific task
                result = await sync_manager.sync_task(int(task_id), "remote_to_local")
                
                # Display result
                if result["status"] == "success":
                    display_success(f"Successfully pulled task {task_id}")
                else:
                    display_error(f"Error pulling task {task_id}: {result.get('message', 'Unknown error')}")
            else:
                # Sync all tasks
                result = await sync_manager.sync_all("remote_to_local")
                
                # Display results
                if result["status"] == "success":
                    display_success("Pull completed")
                    
                    # Create table
                    table = Table(title="Pull Results")
                    table.add_column("Task ID")
                    table.add_column("System")
                    table.add_column("Status")
                    table.add_column("Message")
                    
                    for detail in result.get("details", []):
                        task_id = detail.get("task_id", "")
                        system = detail.get("system", "")
                        status = detail.get("status", "")
                        message = detail.get("message", "")
                        
                        table.add_row(
                            str(task_id),
                            system,
                            status,
                            message
                        )
                    
                    # Display table
                    display_table(table)
                    
                    # Display summary
                    display_info(f"Total tasks: {result.get('total', 0)}")
                    display_info(f"Pulled: {result.get('synced', 0)}")
                    display_info(f"Errors: {result.get('errors', 0)}")
                    display_info(f"Skipped: {result.get('skipped', 0)}")
                else:
                    display_error(f"Error pulling tasks: {result.get('message', 'Unknown error')}")
        finally:
            # Ensure we close any open sessions
            if hasattr(sync_manager, 'adapters') and system in sync_manager.adapters:
                adapter = sync_manager.adapters[system]
                if hasattr(adapter, 'client') and adapter.client:
                    if hasattr(adapter.client, 'session') and adapter.client.session:
                        await adapter.client.session.close()
                        if verbose:
                            display_info("Closed client session")
    
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def link_task(
    task_id: str = typer.Argument(..., help="ID of the task to link"),
    system: str = typer.Option("nextcloud", "--system", "-s", help="External system to link with (e.g., nextcloud)"),
    external_id: str = typer.Option(..., "--external-id", "-e", help="External task ID to link with"),
    calendar: str = typer.Option("Taskinator", "--calendar", "-c", help="Calendar name to use (will be created if it doesn't exist)"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output, including credentials being used"
    ),
):
    """Link a local task with an external task."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get task manager
        task_manager = TaskManager()
        
        # Get configuration for the system
        config = get_sync_config(system)
        
        if verbose:
            display_info(f"Using credentials for {system}:")
            for key, value in config.items():
                if key in ["host", "username"]:
                    display_info(f"  {key}: {value}")
                elif key in ["password", "token"]:
                    if value:
                        display_info(f"  {key}: ***")
                    else:
                        display_info(f"  {key}: <not set>")
            display_info(f"Using calendar: {calendar}")
        
        # Create sync manager
        nextcloud_config = config.get("nextcloud", {})
        sync_manager = SyncManager(
            tasks_file=task_manager.tasks_file,
            nextcloud_host=nextcloud_config.get("host"),
            nextcloud_username=nextcloud_config.get("username"),
            nextcloud_password=nextcloud_config.get("password"),
            nextcloud_token=nextcloud_config.get("token"),
            nextcloud_calendar=calendar,
            verbose=verbose
        )
        
        try:
            # Initialize the sync manager
            await sync_manager.initialize()
            
            # Get task
            task_id = int(task_id)
            task = task_manager.get_task(task_id)
            
            if not task:
                display_error(f"Task {task_id} not found")
                raise typer.Exit(1)
            
            # Link task
            display_info(f"Linking task {task_id} with external task {external_id}...")
            result = await sync_manager.link_task(task, system, external_id)
            
            if result:
                display_success(f"Task {task_id} linked successfully")
                
                # Update task in task manager
                task_manager.update_task(result)
                task_manager.save_tasks()
            else:
                display_error(f"Failed to link task {task_id}")
        finally:
            # Ensure we close any open sessions
            if hasattr(sync_manager, 'adapters') and system in sync_manager.adapters:
                adapter = sync_manager.adapters[system]
                if hasattr(adapter, 'client') and adapter.client:
                    if hasattr(adapter.client, 'session') and adapter.client.session:
                        await adapter.client.session.close()
                        if verbose:
                            display_info("Closed client session")
    
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def resolve(
    task_id: str = typer.Argument(..., help="ID of the task with conflict"),
    system: str = typer.Argument(..., help="External system identifier"),
    resolution: str = typer.Option(
        "local", 
        "--resolution", 
        "-r", 
        help="Conflict resolution strategy (local, remote, merge)"
    ),
    config_file: Path = typer.Option(
        None, 
        "--config", 
        "-c", 
        help="Path to configuration file for external systems"
    )
):
    """Resolve a synchronization conflict."""
    try:
        # Initialize task manager
        task_manager = TaskManager(display_output=True)
        
        # Load config if provided
        config = None
        if config_file:
            if not config_file.exists():
                display_error(f"Config file not found: {config_file}")
                raise typer.Exit(1)
            
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                display_error(f"Invalid JSON in config file: {config_file}")
                raise typer.Exit(1)
        
        # Resolve conflict
        await task_manager.resolve_conflict(task_id, system, resolution, config)
        
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def migrate(
    migration: str = typer.Argument(..., help="Migration to run"),
    tasks_file: Path = typer.Option(None, "--file", "-f", help="Path to tasks.json file")
):
    """Run a database migration."""
    try:
        # Determine tasks file path
        if not tasks_file:
            task_manager = TaskManager(display_output=True)
            tasks_file = task_manager.tasks_file
        
        # Check if migration exists
        try:
            migration_module = importlib.import_module(f"taskinator.migrations.{migration}")
        except ImportError:
            display_error(f"Migration not found: {migration}")
            raise typer.Exit(1)
        
        # Run migration
        display_info(f"Running migration: {migration}")
        migration_module.run_migration(tasks_file)
        display_success(f"Migration completed successfully: {migration}")
        
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

def get_sync_config(system: str) -> Dict[str, Any]:
    """Get configuration for an external system.
    
    Args:
        system: External system name
        
    Returns:
        Configuration dictionary
    """
    import os
    
    # Initialize config
    config = {}
    
    # NextCloud credentials
    if system == "nextcloud":
        nextcloud_host = os.getenv("NEXTCLOUD_HOST")
        nextcloud_username = os.getenv("NEXTCLOUD_USERNAME")
        nextcloud_password = os.getenv("NEXTCLOUD_PASSWORD")
        nextcloud_token = os.getenv("NEXTCLOUD_TOKEN")
        
        # For testing, if no credentials are provided, use dummy values
        if not nextcloud_host:
            log.warning("No NextCloud credentials found in environment, using dummy values for testing")
            nextcloud_host = "https://nextcloud.example.com"
            nextcloud_username = "testuser"
            nextcloud_password = "testpass"
        
        config = {
            "nextcloud": {
                "host": nextcloud_host,
                "username": nextcloud_username,
                "password": nextcloud_password,
                "token": nextcloud_token
            }
        }
    
    return config

def display_sync_results(result):
    """Display synchronization results."""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    console.print()
    console.print("[bold]Synchronization Results:[/bold]")
    console.print("------------------------")
    
    status_color = "green" if result.get("status") == "success" else "red"
    console.print(f"Status: [{status_color}]{result.get('status', 'unknown')}[/{status_color}]")
    
    # Display summary
    console.print(f"Total tasks: {result.get('total', 0)}")
    console.print(f"Synced: {result.get('synced', 0)}")
    console.print(f"Errors: {result.get('errors', 0)}")
    console.print(f"Conflicts: {result.get('conflicts', 0)}")
    console.print(f"Skipped: {result.get('skipped', 0)}")
    
    # Display details if available
    if "details" in result and result["details"]:
        console.print()
        console.print("Details:")
        
        table = Table(show_header=True)
        table.add_column("Task ID")
        table.add_column("System")
        table.add_column("Status")
        table.add_column("Message")
        
        for detail in result["details"]:
            status = detail.get("status", "")
            status_color = "green" if status == "synced" else "red" if status == "error" else "yellow" if status == "conflict" else "dim"
            
            table.add_row(
                str(detail.get("task_id", "")),
                detail.get("system", ""),
                f"[{status_color}]{status}[/{status_color}]",
                detail.get("message", "")
            )
        
        console.print(table)

def display_task_list(tasks, show_details=False):
    """Display a list of tasks in a rich table."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Dependencies", style="blue")
    table.add_column("Sync", style="magenta")
    
    for task in tasks:
        # Format dependencies
        dependencies = ", ".join([str(dep) for dep in task.get("dependencies", [])])
        
        # Get sync status indicators
        sync_status = get_sync_status_indicator(task)
        
        # Add row to table
        table.add_row(
            str(task.get("id", "")),
            task.get("title", ""),
            task.get("status", ""),
            task.get("priority", ""),
            dependencies,
            sync_status
        )
        
        # Show subtasks if requested
        if show_details and "subtasks" in task and task["subtasks"]:
            for subtask in task["subtasks"]:
                # Format subtask dependencies
                subtask_deps = ", ".join([str(dep) for dep in subtask.get("dependencies", [])])
                
                # Get sync status for subtask
                subtask_sync = get_sync_status_indicator(subtask)
                
                # Add subtask row
                table.add_row(
                    f"└─ {subtask.get('id', '')}",
                    f"  {subtask.get('title', '')}",
                    subtask.get("status", ""),
                    subtask.get("priority", ""),
                    subtask_deps,
                    subtask_sync
                )
    
    console = Console()
    console.print(table)

def get_sync_status_indicator(task):
    """Get a visual indicator for the sync status of a task."""
    if "external_sync" not in task or not task["external_sync"]:
        return ""
    
    indicators = []
    for sync_data in task["external_sync"]:
        system = sync_data.get("system", "")
        status = sync_data.get("sync_status", "")
        
        # Create indicator based on system and status
        if system == "nextcloud":
            prefix = "NC"
        elif system == "gitlab":
            prefix = "GL"
        elif system == "azure":
            prefix = "AZ"
        else:
            prefix = system[:2].upper()
        
        if status == "synced":
            indicator = f"[green]{prefix}✓[/green]"
        elif status == "conflict":
            indicator = f"[red]{prefix}![/red]"
        elif status == "pending":
            indicator = f"[yellow]{prefix}⟳[/yellow]"
        elif status == "error":
            indicator = f"[red]{prefix}✗[/red]"
        else:
            indicator = f"[dim]{prefix}?[/dim]"
        
        indicators.append(indicator)
    
    return " ".join(indicators)

def run():
    """Entry point for the CLI."""
    try:
        app()
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        display_error(f"An unexpected error occurred: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    run()