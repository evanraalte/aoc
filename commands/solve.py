"""Solve command - runs AOC solutions with example testing and optional submission."""

import time
import typer
from aocd.models import Puzzle

from utils.parser import parse_puzzle
from utils.display import display_result, console
from core.runner import run


def solve(
    puzzle: str = typer.Argument(..., help="Puzzle in format YYYY/DD[a|b] or file path (e.g., 2024/3a or solutions/2024/03.py)"),
    part: str = typer.Argument(None, help="Part (a or b) - required when using file path"),
    submit_answer: bool = typer.Option(False, "--submit", "-s", help="Submit the answer after solving"),
    skip_examples: bool = typer.Option(False, "--skip-examples", help="Skip running example tests"),
):
    """
    Run an Advent of Code solution for a specific puzzle.

    Examples:
        solve 2024/3a                  - Run year 2024, day 3, part A
        solve 2024/15b -s              - Run and submit year 2024, day 15, part B
        solve solutions/2024/03.py a   - Run from file path (useful for debugging)
    """
    year, day, parsed_part = parse_puzzle(puzzle, require_part=False)

    # Use parsed part if available, otherwise use provided part argument
    if parsed_part is not None:
        part = parsed_part
    elif part is None:
        console.print("[red]Error: Part (a or b) is required[/red]")
        console.print("[yellow]Use format YYYY/DDa or provide part as second argument[/yellow]")
        raise typer.Exit(code=1)

    # Validate part
    if part.lower() not in ["a", "b"]:
        console.print("[red]Error: Part must be 'a' or 'b'[/red]")
        raise typer.Exit(code=1)

    part = part.lower()

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
