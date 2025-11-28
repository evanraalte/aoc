"""Solve command - runs AOC solutions with example testing and optional submission."""

import time
import typer
from aocd.models import Puzzle

from utils.validation import validate_day, validate_part
from utils.display import display_result, console
from core.runner import run


def solve(
    day: int = typer.Argument(..., help="Day of the puzzle (1-25)"),
    year: int = typer.Option(2015, "--year", "-y", help="Year of the puzzle"),
    part: str = typer.Option("a", "--part", "-p", help="Part of the puzzle (a or b)"),
    submit_answer: bool = typer.Option(False, "--submit", "-s", help="Submit the answer after solving"),
    skip_examples: bool = typer.Option(False, "--skip-examples", help="Skip running example tests"),
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

    # Run examples first (if available and not skipped)
    if not skip_examples:
        examples = puzzle.examples
        if examples:
            console.print(f"\n[cyan]🧪 Running {len(examples)} example(s) for Part {part.upper()}...[/cyan]")
            all_passed = True

            for i, example in enumerate(examples, 1):
                # Get expected answer for this part
                expected = example.answer_a if part == "a" else example.answer_b

                if expected is None:
                    console.print(f"[dim]  Example {i}: No expected answer for part {part.upper()}, skipping...[/dim]")
                    continue

                try:
                    result = run(year=year, day=day, part=part, input=example.input_data)

                    if str(result) == str(expected):
                        console.print(f"[green]  ✓ Example {i}: PASSED (got {result})[/green]")
                    else:
                        console.print(f"[red]  ✗ Example {i}: FAILED[/red]")
                        console.print(f"[red]    Expected: {expected}[/red]")
                        console.print(f"[red]    Got:      {result}[/red]")
                        all_passed = False
                except Exception as e:
                    console.print(f"[red]  ✗ Example {i}: ERROR - {e}[/red]")
                    all_passed = False

            if not all_passed:
                console.print(f"\n[red]❌ Some examples failed. Fix your solution before running on real input.[/red]")
                raise typer.Exit(code=1)

            console.print(f"[green]✓ All examples passed![/green]\n")
        else:
            console.print(f"[dim]No examples found for this puzzle[/dim]\n")

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
