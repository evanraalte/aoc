import importlib.util
import sys
import time
from pathlib import Path
from typing import Union
from aocd.models import Puzzle
from dotenv import load_dotenv
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

app = typer.Typer(help="Advent of Code solution runner and manager")
console = Console()

load_dotenv()

# Boilerplate template for new solutions
SOLUTION_TEMPLATE = '''def a(input: str) -> Any:
    """
    Solution for part A.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """

    # TODO: Implement solution for part A

    return 0


def b(input: str) -> Any:
    """
    Solution for part B.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as an int or str
    """

    # TODO: Implement solution for part B

    return 0
'''


def run(year: int, day: int, part: str, input: str) -> Union[int, str]:
    """
    Dynamically import and run a solution module.

    Args:
        year: The year of the puzzle
        day: The day of the puzzle (1-25)
        part: The part of the puzzle ("a" or "b")
        input: The puzzle input data

    Returns:
        The solution answer as an int or string
    """
    # Construct the module path: year/day/{day:02d}-{part}.py
    module_path = Path(__file__).parent / "solutions" / str(year) / f"{day:02d}.py"

    if not module_path.exists():
        console.print(f"[red]Error: Solution file not found at {module_path}[/red]")
        raise typer.Exit(code=1)

    # Load the module dynamically
    module_name = f"{year}.{day:02d}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        console.print(f"[red]Error: Could not load module from {module_path}[/red]")
        raise typer.Exit(code=1)

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Call the part function from the module (a or b)
    if not hasattr(module, part):
        console.print(f"[red]Error: Module {module_path} does not have a '{part}' function[/red]")
        raise typer.Exit(code=1)

    part_function = getattr(module, part)
    result = part_function(input)

    # Handle both int and str return types
    return str(result)


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
    # Validate inputs
    if day < 1 or day > 25:
        console.print("[red]Error: Day must be between 1 and 25[/red]")
        raise typer.Exit(code=1)

    if part.lower() not in ["a", "b"]:
        console.print("[red]Error: Part must be 'a' or 'b'[/red]")
        raise typer.Exit(code=1)

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
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Display result with beautiful formatting
    result_panel = Panel(
        f"[green bold]{answer}[/green bold]",
        title=f"[yellow]Answer - Year {year}, Day {day}, Part {part.upper()}[/yellow]",
        subtitle=f"[dim]⏱️  Completed in {elapsed:.4f}s[/dim]",
        border_style="green"
    )
    console.print("\n")
    console.print(result_panel)
    console.print("\n")

    # Submit if requested
    if submit_answer:
        console.print(f"[cyan]📤 Submitting answer for Year {year}, Day {day}, Part {part.lower()}...[/cyan]")
        try:
            if part == "a":
                puzzle.answer_a = answer
                console.print("[green]✓ Answer submitted successfully![/green]")
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
    # Validate inputs
    if day < 1 or day > 25:
        console.print("[red]Error: Day must be between 1 and 25[/red]")
        raise typer.Exit(code=1)

    # Create directory structure
    solutions_dir = Path(__file__).parent / "solutions" / str(year)
    solutions_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py if it doesn't exist
    init_file = solutions_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")

    # Create solution file
    solution_file = solutions_dir / f"{day:02d}.py"

    if solution_file.exists() and not force:
        console.print(f"[yellow]⚠️  Solution file already exists at {solution_file}[/yellow]")
        console.print("[yellow]Use --force to overwrite[/yellow]")
        raise typer.Exit(code=1)

    solution_file.write_text(SOLUTION_TEMPLATE)

    # Display success message with syntax highlighting
    console.print(f"[green]✓ Created solution file: {solution_file}[/green]\n")
    syntax = Syntax(SOLUTION_TEMPLATE, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="[yellow]Boilerplate Code[/yellow]", border_style="green"))
    console.print(f"\n[cyan]Run with: [bold]python main.py solve {day} --year {year}[/bold][/cyan]")


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
    # Validate inputs
    if day < 1 or day > 25:
        console.print("[red]Error: Day must be between 1 and 25[/red]")
        raise typer.Exit(code=1)

    if part.lower() not in ["a", "b"]:
        console.print("[red]Error: Part must be 'a' or 'b'[/red]")
        raise typer.Exit(code=1)

    # Run the solution with timing
    console.print(f"[cyan]🧪 Testing solution for Year {year}, Day {day}, Part {part.upper()}...[/cyan]")
    start_time = time.perf_counter()
    try:
        answer = run(year=year, day=day, part=part, input=example_input)
    except Exception as e:
        console.print(f"[red]Error running solution: {e}[/red]")
        raise typer.Exit(code=1)
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Display result with beautiful formatting
    result_panel = Panel(
        f"[green bold]{answer}[/green bold]",
        title=f"[yellow]Test Result - Year {year}, Day {day}, Part {part.upper()}[/yellow]",
        subtitle=f"[dim]⏱️  Completed in {elapsed:.4f}s[/dim]",
        border_style="blue"
    )
    console.print("\n")
    console.print(result_panel)
    console.print("\n")


if __name__ == "__main__":
    app()