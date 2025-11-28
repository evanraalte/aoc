"""Test command - tests solutions with example input."""

import time
import typer

from utils.validation import validate_day, validate_part
from utils.display import display_result, console
from core.runner import run


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
