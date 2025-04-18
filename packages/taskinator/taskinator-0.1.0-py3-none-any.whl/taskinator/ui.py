"""Terminal UI components and formatting for Task Blaster."""

from typing import Any, Dict, List, Optional, Tuple, Union

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from .config import TaskPriority, TaskStatus

console = Console()

# Color schemes
COLORS = {
    'status': {
        TaskStatus.PENDING: 'yellow',
        TaskStatus.IN_PROGRESS: 'blue',
        TaskStatus.DONE: 'green',
        TaskStatus.BLOCKED: 'red'
    },
    'priority': {
        TaskPriority.LOW: 'cyan',
        TaskPriority.MEDIUM: 'yellow',
        TaskPriority.HIGH: 'red'
    }
}

def create_loading_indicator(message: str = "Working...") -> Progress:
    """Create a loading indicator with spinner."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    )

def display_banner(title: str = "Task Blaster") -> None:
    """Display the application banner."""
    console.print()
    console.print(Panel(
        Text(title, style="bold blue", justify="center"),
        box=box.DOUBLE,
        expand=False
    ))
    console.print()

def create_task_table(
    tasks: List[Dict[str, Any]],
    show_subtasks: bool = False,
    show_dependencies: bool = True
) -> Table:
    """Create a rich table for displaying tasks."""
    table = Table(
        show_header=True,
        header_style="bold blue",
        box=box.ROUNDED,
        expand=True
    )
    
    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Status", style="white", no_wrap=True)
    table.add_column("Priority", style="white", no_wrap=True)
    if show_dependencies:
        table.add_column("Dependencies", style="white")
    
    # Add rows
    for task in tasks:
        row = [
            str(task['id']),
            task['title'],
            Text(task['status'], style=COLORS['status'].get(task['status'], 'white')),
            Text(task['priority'], style=COLORS['priority'].get(task['priority'], 'white')),
        ]
        
        if show_dependencies:
            deps = format_dependencies(task.get('dependencies', []))
            row.append(deps)
        
        table.add_row(*row)
        
        # Add subtasks if requested
        if show_subtasks and task.get('subtasks'):
            for subtask in task['subtasks']:
                sub_row = [
                    f"  {task['id']}.{subtask['id']}",
                    f"└─ {subtask['title']}",
                    Text(subtask['status'], style=COLORS['status'].get(subtask['status'], 'white')),
                    Text(subtask.get('priority', ''), style=COLORS['priority'].get(subtask.get('priority'), 'white')),
                ]
                
                if show_dependencies:
                    sub_deps = format_dependencies(subtask.get('dependencies', []))
                    sub_row.append(sub_deps)
                
                table.add_row(*sub_row)
    
    return table

def format_dependencies(
    dependencies: List[Union[str, int]],
    tasks: Optional[List[Dict[str, Any]]] = None
) -> Text:
    """Format task dependencies with status colors if tasks are provided."""
    if not dependencies:
        return Text("None", style="dim")
    
    result = Text()
    for i, dep in enumerate(dependencies):
        if i > 0:
            result.append(", ")
        
        if tasks:
            # Find the dependency's status
            for task in tasks:
                if str(task['id']) == str(dep):
                    status = task.get('status', TaskStatus.PENDING)
                    result.append(
                        str(dep),
                        style=COLORS['status'].get(status, 'white')
                    )
                    break
            else:
                # Dependency not found
                result.append(str(dep), style="red")
        else:
            # No tasks provided, just show the ID
            result.append(str(dep))
    
    return result

def display_task_details(task: Dict[str, Any]) -> None:
    """Display detailed information about a task."""
    console.print(Panel(
        Text.from_markup(f"""
[bold cyan]Task {task['id']}[/bold cyan]: {task['title']}
[bold]Status:[/bold] {Text(task['status'], style=COLORS['status'].get(task['status'], 'white'))}
[bold]Priority:[/bold] {Text(task['priority'], style=COLORS['priority'].get(task['priority'], 'white'))}
[bold]Dependencies:[/bold] {format_dependencies(task.get('dependencies', []))}

[bold]Description:[/bold]
{task.get('description', 'No description provided.')}

[bold]Details:[/bold]
{task.get('details', 'No details provided.')}

[bold]Test Strategy:[/bold]
{task.get('testStrategy', 'No test strategy provided.')}
        """.strip()),
        title=f"Task Details",
        box=box.ROUNDED,
        expand=False
    ))
    
    if task.get('subtasks'):
        console.print()
        console.print(Panel(
            create_task_table(task['subtasks'], show_subtasks=False),
            title="Subtasks",
            box=box.ROUNDED,
            expand=False
        ))

def display_error(message: str) -> None:
    """Display an error message."""
    console.print(Panel(
        Text(message, style="red"),
        title="Error",
        box=box.ROUNDED,
        border_style="red",
        expand=False
    ))

def display_success(message: str) -> None:
    """Display a success message."""
    console.print(Panel(
        Text(message, style="green"),
        title="Success",
        box=box.ROUNDED,
        border_style="green",
        expand=False
    ))

def display_info(message: str) -> None:
    """Display an informational message."""
    console.print(f"[blue]{message}[/blue]")

def display_table(table: Table) -> None:
    """Display a Rich table."""
    console.print(table)