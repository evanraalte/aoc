"""Path and file utilities."""

from pathlib import Path


def get_solution_path(year: int, day: int) -> Path:
    """
    Get the path to a solution file.

    Args:
        year: The year of the puzzle
        day: The day of the puzzle

    Returns:
        Path to the solution file
    """
    return Path(__file__).parent.parent / "solutions" / str(year) / f"{day:02d}.py"


def ensure_solution_directory(year: int) -> Path:
    """
    Ensure the solution directory exists and has an __init__.py file.

    Args:
        year: The year of the puzzle

    Returns:
        Path to the solution directory
    """
    solutions_dir = Path(__file__).parent.parent / "solutions" / str(year)
    solutions_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py if it doesn't exist
    init_file = solutions_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")

    return solutions_dir
