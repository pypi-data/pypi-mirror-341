# OneRead

A terminal utility to display one daily article for "positive news" and "scientific interviews".

## Installation

### Install from PyPI (Recommended)

```bash
# Install using pip
pip install oneread

# Or install globally using pipx
pipx install oneread
```

### Install from Source

You can also install OneRead directly from the source:

```bash
# Clone the repository
git clone https://github.com/decodingchris/OneRead.git
cd OneRead

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the package
pip install -e .
```

## Usage

OneRead provides several commands to fetch and display articles:

### Show articles from all categories

```bash
oneread
```

### Read an article from a specific category

```bash
oneread <category>
```

For example:

```bash
oneread positive
oneread science
```

### List available categories

```bash
oneread list
```

### Show help information

```bash
oneread help
```

## Features

- Fetches articles from the DayGrab GitHub repository
- Displays content in a nicely formatted way with colors and styling
- Shows all available articles from different categories
- Handles errors gracefully with fallback options
- Indicates when backup content is being used

## Requirements

- Python 3.10 or higher
- Internet connection to fetch articles from GitHub

## Dependencies

- requests: For making HTTP requests to the GitHub API
- rich: For terminal formatting and styling
- click: For command-line interface

## Development

### Linting

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and code formatting. Ruff is configured in the `pyproject.toml` file.

To check your code for linting issues:

```bash
ruff check .
```

To automatically fix most linting issues:

```bash
ruff check --fix .
```

The project follows these linting rules:

- E: pycodestyle errors
- F: pyflakes errors
- W: pycodestyle warnings
- I: isort
- B: flake8-bugbear
- C4: flake8-comprehensions

### Testing

Run tests with pytest:

```bash
pytest
```

Check test coverage:

```bash
pytest --cov=oneread
```
