"""Input validation utilities."""

import typer
from rich.console import Console

console = Console()


def validate_day(day: int) -> None:
    """
    Validate that day is between 1 and 25.

    Args:
        day: The day to validate

    Raises:
        typer.Exit: If day is invalid
    """
    if day < 1 or day > 25:
        console.print("[red]Error: Day must be between 1 and 25[/red]")
        raise typer.Exit(code=1)


def validate_part(part: str) -> None:
    """
    Validate that part is 'a' or 'b'.

    Args:
        part: The part to validate

    Raises:
        typer.Exit: If part is invalid
    """
    if part.lower() not in ["a", "b"]:
        console.print("[red]Error: Part must be 'a' or 'b'[/red]")
        raise typer.Exit(code=1)
