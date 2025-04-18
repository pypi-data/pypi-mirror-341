"""Command-line interface for OneRead."""

import json
import sys
from typing import Dict, List, Optional

import click
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

# Initialize rich console
console = Console()

# GitHub API URLs
REPO_API_URL = "https://api.github.com/repos/decodingchris/DayGrab/contents/articles"

# Known categories (fallback)
KNOWN_CATEGORIES = ["positive", "science"]


def fetch_categories() -> List[str]:
    """Fetch all available categories from the GitHub repository."""
    try:
        response = requests.get(
            REPO_API_URL,
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10,
        )
        response.raise_for_status()

        categories = [
            item["name"] for item in response.json() if item["type"] == "dir"
        ]
        return categories
    except (requests.RequestException, json.JSONDecodeError) as e:
        console.print(f"[bold red]Error fetching categories:[/] {str(e)}")
        console.print("[yellow]Falling back to known categories.[/]")
        return KNOWN_CATEGORIES


def get_article_download_url(category: str) -> Optional[str]:
    """Get the download URL for an article JSON file."""
    category_url = f"{REPO_API_URL}/{category}"

    try:
        response = requests.get(
            category_url,
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10,
        )
        response.raise_for_status()

        # Find the daily article JSON file
        file_name = f"daily_{category}_article.json"
        for item in response.json():
            if item["name"] == file_name and item["type"] == "file":
                return item["download_url"]

        console.print(f"[bold red]Error:[/] Could not find {file_name} in {category}")
        return None
    except (requests.RequestException, json.JSONDecodeError) as e:
        console.print(f"[bold red]Error getting article URL:[/] {str(e)}")
        return None


def fetch_article(category: str) -> Optional[Dict]:
    """Fetch article from a specific category."""
    download_url = get_article_download_url(category)

    if not download_url:
        return None

    try:
        response = requests.get(download_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching article from {category}:[/] {str(e)}")
        return None
    except json.JSONDecodeError:
        console.print(f"[bold red]Error:[/] Invalid JSON in {category} article")
        return None


def display_article(article: Dict, category: str) -> None:
    """Display an article in a nicely formatted way."""
    if not article:
        return

    # Get article data
    text = article.get("text", "No content available")
    source = article.get("source", "Unknown source")
    source_type = article.get("source_type", "unknown")
    status = article.get("status", "none")
    date = article.get("date", "Unknown date")

    # Create title
    title = Text(f"{category.upper()} ARTICLE", style="bold cyan")

    # Create content based on status
    if status == "feed":
        # If status is feed, text is the title and source is the URL
        content = f"# {text}\n\n"
        if source_type == "url":
            content += f"[Read more at the source]({source})\n\n"
        else:
            content += f"Source: {source}\n\n"
    else:
        # If status is backup or none, text is the full content
        content = text
        content += f"\n\nSource: {source}"

        # Add note about backup article
        if status == "backup":
            content += "\n\nNote: This is backup content as no article of the day was available."

    # Add date
    content += f"\n\nDate: {date}"

    # Display in a panel
    md = Markdown(content)
    console.print(Panel(md, title=title, expand=False))


def show_help():
    """Show help information."""
    console.print("[bold]OneRead - A terminal utility to display one daily article for[/] "
                  "[bold]'positive news' and 'scientific interviews'.[/]")
    console.print("\n[bold]Available commands:[/]")
    console.print("  [green]oneread[/]               Show articles from all categories")
    console.print("  [green]oneread <category>[/]    Read an article from a specific category")
    console.print("  [green]oneread list[/]          List all available categories")
    console.print("  [green]oneread help[/]          Show this help message")

    console.print("\n[bold]Examples:[/]")
    console.print("  [dim]oneread[/]")
    console.print("  [dim]oneread positive[/]")
    console.print("  [dim]oneread science[/]")
    console.print("  [dim]oneread list[/]")


def show_all_articles():
    """Show articles from all available categories."""
    categories = fetch_categories()

    if not categories:
        console.print("[bold red]No categories found.[/]")
        return

    for category in categories:
        with console.status(f"Fetching article from {category}...", spinner="dots"):
            article = fetch_article(category)

        if article:
            display_article(article, category)
            # Add a separator between articles
            if category != categories[-1]:
                console.print("\n---\n")
        else:
            console.print(f"[bold red]No article found for category: {category}[/]")


def read_category_article(category):
    """Read an article from a specific category."""
    with console.status(f"Fetching article from {category}...", spinner="dots"):
        article = fetch_article(category)

    if article:
        display_article(article, category)
    else:
        console.print(f"[bold red]No article found for category: {category}[/]")
        categories = fetch_categories()
        if categories:
            console.print("\n[bold]Available categories:[/]")
            for cat in categories:
                console.print(f"[green]- {cat}[/]")


# Create a custom multi-command class that handles category names
class OneReadCLI(click.Group):
    def get_command(self, ctx, cmd_name):
        # First, try to get a standard command
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # If not a standard command, treat it as a category name
        return click.Command(
            name=cmd_name,
            callback=lambda: read_category_article(cmd_name),
            help=f"Read an article from the {cmd_name} category",
        )


@click.group(cls=OneReadCLI, invoke_without_command=True)
@click.version_option(version="1.0.0")
@click.pass_context
def cli(ctx):
    """OneRead - A terminal utility to display one daily article.

    For 'positive news' and 'scientific interviews'.
    """
    # If no subcommand is provided, show all articles
    if ctx.invoked_subcommand is None:
        show_all_articles()


@cli.command()
def list():
    """List all available article categories."""
    categories = fetch_categories()

    console.print("[bold]Available categories:[/]")
    for category in categories:
        console.print(f"[green]- {category}[/]")

    console.print("\n[dim]Use 'oneread <category>' to read an article from a specific category[/]")


@cli.command()
def help():
    """Show help information."""
    show_help()


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
