"""New command - creates solution files from boilerplate template."""

import typer
from rich.panel import Panel
from rich.syntax import Syntax

from utils.parser import parse_puzzle
from utils.paths import get_solution_path, ensure_solution_directory
from utils.display import console
from templates import SOLUTION_TEMPLATE


def new(
    puzzle: str = typer.Argument(..., help="Puzzle in format YYYY/DD (e.g., 2024/3)"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing file"),
):
    """
    Create a new solution file from boilerplate template.

    Examples:
        new 2024/3       - Create solution file for year 2024, day 3
        new 2024/15 -f   - Force overwrite existing file
    """
    year, day, _ = parse_puzzle(puzzle, require_part=False)

    # Ensure directory structure exists
    ensure_solution_directory(year)

    # Get solution file path
    solution_file = get_solution_path(year, day)

    if solution_file.exists() and not force:
        console.print(f"[yellow]⚠️  Solution file already exists at {solution_file}[/yellow]")
        console.print("[yellow]Use --force to overwrite[/yellow]")
        raise typer.Exit(code=1)

    # Create the file
    solution_file.write_text(SOLUTION_TEMPLATE)

    # Display success message with syntax highlighting
    console.print(f"[green]✓ Created solution file: {solution_file}[/green]\n")
    syntax = Syntax(SOLUTION_TEMPLATE, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="[yellow]Boilerplate Code[/yellow]", border_style="green"))
    console.print(f"\n[cyan]Run with: [bold]uv run main.py solve {year}/{day}a[/bold][/cyan]")
