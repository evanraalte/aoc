# Advent of Code Solution Runner

A beautiful CLI tool for managing and running Advent of Code solutions with rich formatting, timing, and automatic submission.

## Features

- 🚀 **Fast solution runner** with automatic input fetching
- 📦 **Boilerplate generator** for quick solution scaffolding
- ⏱️ **Performance timing** to optimize your solutions
- 🎨 **Rich terminal output** with colors and formatting
- 🧪 **Automatic example testing** validates solutions before running on real input
- 🧪 **Testing framework** for custom example inputs
- 📤 **Automatic submission** to Advent of Code
- 💾 **Organized structure** with year/day solution files
- 📁 **Modular codebase** with clean separation of concerns

## Installation

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone or create your repository:
```bash
git clone <your-repo> aoc
cd aoc
```

2. Install dependencies:
```bash
uv sync
```

3. Configure your Advent of Code session:
Create a `.env` file in the project root:
```bash
AOC_SESSION=your_session_cookie_here
```

To get your session cookie:
- Log in to [Advent of Code](https://adventofcode.com)
- Open browser DevTools (F12)
- Go to Application/Storage → Cookies
- Copy the value of the `session` cookie

## Usage

### Create a New Solution

Generate boilerplate code for a new day:

```bash
# Create solution for day 5 of year 2023
uv run main.py new 5 --year 2023

# Short form
uv run main.py new 5 -y 2023

# Overwrite existing file
uv run main.py new 5 -y 2023 --force
```

This creates a file at `solutions/2023/05.py` with template code for both parts A and B.

### Run a Solution

Execute a solution with automatic input fetching:

```bash
# Run day 1, part A for year 2023
uv run main.py solve 1 --year 2023 --part a

# Short form
uv run main.py solve 1 -y 2023 -p a

# Default year is 2015, default part is 'a'
uv run main.py solve 1

# Run part B
uv run main.py solve 1 -y 2023 -p b

# Skip example tests (run only on real input)
uv run main.py solve 1 -y 2023 -p a --skip-examples
```

Features:
- Automatically fetches your puzzle input
- Runs example tests first and validates your solution
- Only proceeds to real input if all examples pass
- Times solution execution
- Displays result in a beautiful panel

### Test with Example Input

Test your solution with example data before running on real input:

```bash
# Test with example input
uv run main.py test 1 "1abc2\npqr3stu8vwx\na1b2c3d4e5f" -y 2023 -p a

# Test part B
uv run main.py test 1 "example input here" -y 2023 -p b
```

### Submit Answer

Submit your answer directly to Advent of Code:

```bash
# Run and submit in one command
uv run main.py solve 1 -y 2023 -p a --submit

# Short form
uv run main.py solve 1 -y 2023 -p a -s
```

### Get Help

```bash
# General help
uv run main.py --help

# Command-specific help
uv run main.py solve --help
uv run main.py new --help
uv run main.py test --help
```

## Project Structure

```
aoc/
├── .env                    # Your AOC session token (gitignored)
├── .gitignore             # Ignore patterns
├── main.py                # CLI entry point (app setup and command registration)
├── templates.py           # Solution file templates
├── pyproject.toml         # Project dependencies
├── README.md              # This file
├── commands/              # CLI command modules
│   ├── __init__.py
│   ├── solve.py           # Solve command (run solutions with example testing)
│   ├── new.py             # New command (create boilerplate)
│   └── test.py            # Test command (test with custom input)
├── core/                  # Core functionality
│   ├── __init__.py
│   └── runner.py          # Solution execution logic
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── validation.py      # Input validation
│   ├── paths.py           # Path and file helpers
│   └── display.py         # Display and formatting
└── solutions/             # Your solutions
    ├── 2015/
    │   ├── __init__.py
    │   ├── 01.py
    │   ├── 02.py
    │   └── ...
    ├── 2023/
    │   ├── __init__.py
    │   └── 01.py
    └── ...
```

### Module Overview

- **main.py** - Minimal CLI entry point that registers commands
- **templates.py** - Boilerplate code templates for new solutions
- **commands/solve.py** - Solve command with example testing and submission
- **commands/new.py** - New command for creating solution files
- **commands/test.py** - Test command for running with custom input
- **core/runner.py** - Dynamic module loading and solution execution
- **utils/validation.py** - Input validation (day, part)
- **utils/paths.py** - File path management and directory creation
- **utils/display.py** - Rich console output formatting

## Solution File Format

Each solution file should have two functions: `a()` and `b()` for parts A and B:

```python
from typing import Any


def a(input: str) -> Any:
    """
    Solution for part A.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """
    lines = input.strip().splitlines()

    # TODO: Implement solution for part A

    return 0


def b(input: str) -> Any:
    """
    Solution for part B.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """
    lines = input.strip().splitlines()

    # TODO: Implement solution for part B

    return 0
```

## Tips

- Use `uv run main.py new <day>` to quickly scaffold new solutions
- The `solve` command automatically runs example tests first to validate your solution
- Use `--skip-examples` if you want to bypass example tests
- Test with custom inputs using the `test` command
- The tool automatically handles any return type that can be converted to string
- Execution time is displayed to help you optimize solutions
- Use `--submit` carefully - you have limited incorrect attempts per day!

## Dependencies

- `typer` - Beautiful CLI framework
- `rich` - Terminal formatting and colors
- `advent-of-code-data` - AOC input fetching and submission
- `python-dotenv` - Environment variable management

## License

MIT

## Contributing

Feel free to fork and customize for your own Advent of Code journey!
