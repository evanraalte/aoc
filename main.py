"""Advent of Code CLI - Main entry point."""

from dotenv import load_dotenv
import typer

from commands.solve import solve
from commands.new import new

load_dotenv()

app = typer.Typer(help="Advent of Code solution runner and manager")

# Register commands
app.command()(solve)
app.command()(new)


if __name__ == "__main__":
    app()
