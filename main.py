import importlib.util
import sys
from pathlib import Path
from aocd.models import Puzzle
from dotenv import load_dotenv
import typer

app = typer.Typer()

load_dotenv()


def run(year: int, day: int, part: str, input: str) -> str:
    """
    Dynamically import and run a solution module.

    Args:
        year: The year of the puzzle
        day: The day of the puzzle (1-25)
        part: The part of the puzzle ("a" or "b")
        input: The puzzle input data

    Returns:
        The solution answer as a string
    """
    # Construct the module path: year/day/{day:02d}-{part}.py
    module_path = Path(__file__).parent / "solutions" / str(year) / f"{day:02d}.py"

    if not module_path.exists():
        typer.echo(f"Error: Solution file not found at {module_path}", err=True)
        raise typer.Exit(code=1)

    # Load the module dynamically
    module_name = f"{year}.{day:02d}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        typer.echo(f"Error: Could not load module from {module_path}", err=True)
        raise typer.Exit(code=1)

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Call the part function from the module (a or b)
    if not hasattr(module, part):
        typer.echo(f"Error: Module {module_path} does not have a '{part}' function", err=True)
        raise typer.Exit(code=1)

    part_function = getattr(module, part)
    return part_function(input)


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
        typer.echo("Error: Day must be between 1 and 25", err=True)
        raise typer.Exit(code=1)

    if part.lower() not in ["a", "b"]:
        typer.echo("Error: Part must be 'a' or 'b'", err=True)
        raise typer.Exit(code=1)

    # Get puzzle input
    typer.echo(f"Fetching input for Year {year}, Day {day}...")
    try:
        puzzle = Puzzle(day=day, year=year)
    except Exception as e:
        typer.echo(f"Error fetching input: {e}", err=True)
        raise typer.Exit(code=1)

    # Run the solution
    typer.echo(f"Running solution for Year {year}, Day {day}, Part {part.upper()}...")
    try:
        answer = run(year=year, day=day, part=part, input=puzzle.input_data)
    except Exception as e:
        typer.echo(f"Error running solution: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"\n{'='*50}")
    typer.echo(f"Answer: {answer}")
    typer.echo(f"{'='*50}\n")

    # Submit if requested
    if submit_answer:
        typer.echo(f"Submitting answer for Year {year}, Day {day}, Part {part.lower()}...")
        try:
            if part == "a":
                result = puzzle.answer_a = answer
            else:
                result = puzzle.answer_b = answer
            typer.echo(f"Submission result: {result}")
        except Exception as e:
            typer.echo(f"Error submitting answer: {e}", err=True)
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()