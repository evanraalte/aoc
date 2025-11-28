"""Parse puzzle identifiers in YYYY/D[D][a|b] format or file paths."""

import re
import typer
from typing import Optional, Tuple
from pathlib import Path

from utils.display import console


def parse_puzzle(puzzle: str, require_part: bool = True) -> Tuple[int, int, Optional[str]]:
    """
    Parse a puzzle identifier in the format YYYY/D[D][a|b] or from a file path.

    Formats supported:
        2024/3a              -> (2024, 3, 'a')
        2024/15b             -> (2024, 15, 'b')
        2024/3               -> (2024, 3, None)  # only valid if require_part=False
        solutions/2024/03.py -> (2024, 3, None)  # extracts from file path

    Args:
        puzzle: Puzzle identifier string or file path
        require_part: Whether part (a/b) is required

    Returns:
        Tuple of (year, day, part)

    Raises:
        typer.Exit if format is invalid
    """
    # Check if it's a file path (contains .py or solutions/)
    if '.py' in puzzle or 'solutions/' in puzzle or puzzle.startswith('solutions'):
        # Extract from file path: solutions/2024/03.py -> year=2024, day=3
        path_pattern = r'solutions[/\\](\d{4})[/\\](\d{1,2})\.py'
        match = re.search(path_pattern, puzzle)
        if match:
            year = int(match.group(1))
            day = int(match.group(2))
            part = None  # Part comes from separate argument in debug config

            # Validate day range
            if day < 1 or day > 25:
                console.print(f"[red]Error: Day must be between 1 and 25, got {day}[/red]")
                raise typer.Exit(code=1)

            return year, day, part
        else:
            console.print(f"[red]Error: Invalid file path format '{puzzle}'[/red]")
            console.print("[yellow]Expected: solutions/YYYY/DD.py[/yellow]")
            raise typer.Exit(code=1)

    # Pattern: YYYY/D[D][a|b]
    pattern = r'^(\d{4})/(\d{1,2})([ab])?$'
    match = re.match(pattern, puzzle)

    if not match:
        console.print(f"[red]Error: Invalid puzzle format '{puzzle}'[/red]")
        console.print("[yellow]Expected format: YYYY/DD[a|b] (e.g., 2024/3a, 2024/15b)[/yellow]")
        raise typer.Exit(code=1)

    year = int(match.group(1))
    day = int(match.group(2))
    part = match.group(3)

    # Validate day range
    if day < 1 or day > 25:
        console.print(f"[red]Error: Day must be between 1 and 25, got {day}[/red]")
        raise typer.Exit(code=1)

    # Check if part is required
    if require_part and part is None:
        console.print(f"[red]Error: Part (a or b) is required[/red]")
        console.print("[yellow]Expected format: YYYY/DDa or YYYY/DDb (e.g., 2024/3a)[/yellow]")
        raise typer.Exit(code=1)

    return year, day, part
