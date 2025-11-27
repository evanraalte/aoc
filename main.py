"""Advent of Code CLI - Main entry point."""

import time
from dotenv import load_dotenv
import typer
from aocd.models import Puzzle
from rich.panel import Panel
from rich.syntax import Syntax

from utils.validation import validate_day, validate_part
from utils.paths import get_solution_path, ensure_solution_directory
from utils.display import display_result, console
from core.runner import run
from templates import SOLUTION_TEMPLATE

load_dotenv()

app = typer.Typer(help="Advent of Code solution runner and manager")


# ============================================================================
# CLI Commands
# ============================================================================

@app.command()
def solve(
    day: int = typer.Argument(..., help="Day of the puzzle (1-25)"),
    year: int = typer.Option(2015, "--year", "-y", help="Year of the puzzle"),
    part: str = typer.Option("a", "--part", "-p", help="Part of the puzzle (a or b)"),
    submit_answer: bool = typer.Option(False, "--submit", "-s", help="Submit the answer after solving"),
):
    """
    Run an Advent of Code solution for a specific day, year, and part.
    """
    validate_day(day)
    validate_part(part)

    # Get puzzle input
    console.print(f"[cyan]📥 Fetching input for Year {year}, Day {day}...[/cyan]")
    try:
        puzzle = Puzzle(day=day, year=year)
    except Exception as e:
        console.print(f"[red]Error fetching input: {e}[/red]")
        raise typer.Exit(code=1)

    # Run the solution with timing
    console.print(f"[cyan]🚀 Running solution for Year {year}, Day {day}, Part {part.upper()}...[/cyan]")
    start_time = time.perf_counter()
    try:
        answer = run(year=year, day=day, part=part, input=puzzle.input_data)
    except Exception as e:
        console.print(f"[red]Error running solution: {e}[/red]")
        raise typer.Exit(code=1)
    elapsed = time.perf_counter() - start_time

    # Display result
    display_result(answer, year, day, part, elapsed)

    # Submit if requested
    if submit_answer:
        console.print(f"[cyan]📤 Submitting answer for Year {year}, Day {day}, Part {part.lower()}...[/cyan]")
        try:
            if part == "a":
                puzzle.answer_a = answer
            else:
                puzzle.answer_b = answer
            console.print("[green]✓ Answer submitted successfully![/green]")
        except Exception as e:
            console.print(f"[red]Error submitting answer: {e}[/red]")
            raise typer.Exit(code=1)


@app.command()
def new(
    day: int = typer.Argument(..., help="Day of the puzzle (1-25)"),
    year: int = typer.Option(2015, "--year", "-y", help="Year of the puzzle"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing file"),
):
    """
    Create a new solution file from boilerplate template.
    """
    validate_day(day)

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
    console.print(f"\n[cyan]Run with: [bold]uv run main.py solve {day} --year {year}[/bold][/cyan]")


@app.command()
def test(
    day: int = typer.Argument(..., help="Day of the puzzle (1-25)"),
    example_input: str = typer.Argument(..., help="Example input for testing"),
    year: int = typer.Option(2015, "--year", "-y", help="Year of the puzzle"),
    part: str = typer.Option("a", "--part", "-p", help="Part of the puzzle (a or b)"),
):
    """
    Test a solution with example input.
    """
    validate_day(day)
    validate_part(part)

    # Run the solution with timing
    console.print(f"[cyan]🧪 Testing solution for Year {year}, Day {day}, Part {part.upper()}...[/cyan]")
    start_time = time.perf_counter()
    try:
        answer = run(year=year, day=day, part=part, input=example_input)
    except Exception as e:
        console.print(f"[red]Error running solution: {e}[/red]")
        raise typer.Exit(code=1)
    elapsed = time.perf_counter() - start_time

    # Display result
    display_result(answer, year, day, part, elapsed, title_prefix="Test Result", border_style="blue")


if __name__ == "__main__":
    app()
