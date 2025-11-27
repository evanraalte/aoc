"""Display and output utilities."""

from rich.console import Console
from rich.panel import Panel

console = Console()


def display_result(
    answer: str,
    year: int,
    day: int,
    part: str,
    elapsed: float,
    title_prefix: str = "Answer",
    border_style: str = "green"
) -> None:
    """
    Display a formatted result panel.

    Args:
        answer: The answer to display
        year: The year of the puzzle
        day: The day of the puzzle
        part: The part of the puzzle
        elapsed: Time elapsed in seconds
        title_prefix: Prefix for the panel title
        border_style: Color style for the border
    """
    result_panel = Panel(
        f"[green bold]{answer}[/green bold]",
        title=f"[yellow]{title_prefix} - Year {year}, Day {day}, Part {part.upper()}[/yellow]",
        subtitle=f"[dim]⏱️  Completed in {elapsed:.4f}s[/dim]",
        border_style=border_style
    )
    console.print("\n")
    console.print(result_panel)
    console.print("\n")
