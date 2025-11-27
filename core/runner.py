"""Solution execution module."""

import importlib.util
import sys
import typer
from rich.console import Console

from utils.paths import get_solution_path

console = Console()


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
    module_path = get_solution_path(year, day)

    if not module_path.exists():
        console.print(f"[red]Error: Solution file not found at {module_path}[/red]")
        raise typer.Exit(code=1)

    # Load the module dynamically
    module_name = f"solutions.{year}.{day:02d}"
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

    # Convert result to string (handles any type that can be stringified)
    return str(result)
