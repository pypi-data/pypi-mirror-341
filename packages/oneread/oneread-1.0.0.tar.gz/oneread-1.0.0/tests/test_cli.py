"""Tests for the OneRead CLI module."""

import json
import os
from unittest.mock import MagicMock, patch

import pytest
import requests
from click.testing import CliRunner

from oneread.cli import (
    KNOWN_CATEGORIES,
    cli,
    display_article,
    fetch_article,
    fetch_categories,
    get_article_download_url,
    main,
    read_category_article,
    show_all_articles,
)


@pytest.fixture
def runner():
    """Provide a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def mock_categories_response():
    """Mock response for categories API call."""
    return [
        {"name": "positive", "type": "dir", "path": "articles/positive"},
        {"name": "science", "type": "dir", "path": "articles/science"},
    ]


@pytest.fixture
def mock_article_files_response():
    """Mock response for article files API call."""
    return [
        {
            "name": "daily_positive_article.json",
            "type": "file",
            "download_url": "https://raw.githubusercontent.com/user/repo/main/articles/positive/daily_positive_article.json",
        }
    ]


@pytest.fixture
def mock_article_content():
    """Mock article content."""
    return {
        "text": "Test article content",
        "source": "https://example.com",
        "source_type": "url",
        "status": "feed",
        "date": "2025-04-17",
    }


def test_version(runner):
    """Test the version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


@patch("oneread.cli.requests.get")
def test_fetch_categories(mock_get, mock_categories_response):
    """Test fetching categories."""
    mock_response = MagicMock()
    mock_response.json.return_value = mock_categories_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    categories = fetch_categories()
    assert categories == ["positive", "science"]
    mock_get.assert_called_once()


@patch("oneread.cli.requests.get")
def test_fetch_categories_exception(mock_get):
    """Test fetching categories with an exception."""
    mock_get.side_effect = requests.RequestException("Connection error")

    categories = fetch_categories()
    assert categories == ["positive", "science"]
    assert categories == KNOWN_CATEGORIES


@patch("oneread.cli.requests.get")
def test_get_article_download_url(mock_get, mock_article_files_response):
    """Test getting article download URL."""
    mock_response = MagicMock()
    mock_response.json.return_value = mock_article_files_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    url = get_article_download_url("positive")
    assert url == "https://raw.githubusercontent.com/user/repo/main/articles/positive/daily_positive_article.json"
    mock_get.assert_called_once()


@patch("oneread.cli.requests.get")
def test_get_article_download_url_not_found(mock_get):
    """Test getting article download URL when file not found."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    url = get_article_download_url("positive")
    assert url is None


@patch("oneread.cli.requests.get")
def test_get_article_download_url_error(mock_get):
    """Test getting article download URL with request error."""
    mock_get.side_effect = requests.RequestException("Connection error")

    url = get_article_download_url("positive")
    assert url is None


@patch("oneread.cli.get_article_download_url")
@patch("oneread.cli.requests.get")
def test_fetch_article(mock_get, mock_download_url, mock_article_content):
    """Test fetching an article."""
    mock_download_url.return_value = "https://example.com/article.json"

    mock_response = MagicMock()
    mock_response.json.return_value = mock_article_content
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    article = fetch_article("positive")
    assert article == mock_article_content
    mock_get.assert_called_once_with("https://example.com/article.json", timeout=10)


@patch("oneread.cli.get_article_download_url")
def test_fetch_article_no_url(mock_download_url):
    """Test fetching an article with no download URL."""
    mock_download_url.return_value = None

    article = fetch_article("positive")
    assert article is None


@patch("oneread.cli.get_article_download_url")
@patch("oneread.cli.requests.get")
def test_fetch_article_request_error(mock_get, mock_download_url):
    """Test fetching an article with request error."""
    mock_download_url.return_value = "https://example.com/article.json"
    mock_get.side_effect = requests.RequestException("Connection error")

    article = fetch_article("positive")
    assert article is None


@patch("oneread.cli.get_article_download_url")
@patch("oneread.cli.requests.get")
def test_fetch_article_json_error(mock_get, mock_download_url):
    """Test fetching an article with JSON decode error."""
    mock_download_url.return_value = "https://example.com/article.json"

    mock_response = MagicMock()
    mock_response.json.side_effect = json.JSONDecodeError("JSON decode error", "", 0)
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    article = fetch_article("positive")
    assert article is None


def test_display_article(capsys, mock_article_content):
    """Test displaying an article."""
    display_article(mock_article_content, "positive")
    captured = capsys.readouterr()
    assert "POSITIVE ARTICLE" in captured.out
    assert "Test article content" in captured.out


def test_display_article_backup(capsys):
    """Test displaying a backup article."""
    article = {
        "text": "Backup content",
        "source": "Backup source",
        "source_type": "text",
        "status": "backup",
        "date": "2025-04-17",
    }
    display_article(article, "positive")
    captured = capsys.readouterr()
    assert "POSITIVE ARTICLE" in captured.out
    assert "Backup content" in captured.out
    assert "This is backup content" in captured.out


def test_display_article_none(capsys):
    """Test displaying a None article."""
    # Call the function with an empty dict, which will trigger the early return
    # This is equivalent to None for the 'if not article:' check
    display_article({}, "positive")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_display_article_empty(capsys):
    """Test displaying an empty article."""
    # The function checks if article is None or Falsy, not if it's an empty dict
    # So we need to provide a dict with the expected keys but empty values
    article = {
        "text": "",
        "source": "",
        "source_type": "",
        "status": "",
        "date": "",
    }
    display_article(article, "positive")
    captured = capsys.readouterr()
    assert "POSITIVE ARTICLE" in captured.out
    # It will use the empty string, not the default
    assert "No content available" not in captured.out


def test_display_article_non_url_source(capsys):
    """Test displaying an article with a non-URL source."""
    article = {
        "text": "Test article content",
        "source": "Test source",
        "source_type": "text",  # Not a URL
        "status": "feed",
        "date": "2025-04-17",
    }
    display_article(article, "positive")
    captured = capsys.readouterr()
    assert "POSITIVE ARTICLE" in captured.out
    assert "Source: Test source" in captured.out


@patch("oneread.cli.fetch_categories")
@patch("oneread.cli.fetch_article")
def test_show_all_articles(mock_fetch_article, mock_fetch_categories, mock_article_content):
    """Test showing all articles."""
    mock_fetch_categories.return_value = ["positive", "science"]
    mock_fetch_article.return_value = mock_article_content

    show_all_articles()

    mock_fetch_categories.assert_called_once()
    assert mock_fetch_article.call_count == 2


@patch("oneread.cli.fetch_categories")
def test_show_all_articles_no_categories(mock_fetch_categories, capsys):
    """Test showing all articles when no categories are found."""
    mock_fetch_categories.return_value = []

    show_all_articles()

    captured = capsys.readouterr()
    assert "No categories found" in captured.out
    mock_fetch_categories.assert_called_once()


@patch("oneread.cli.fetch_categories")
@patch("oneread.cli.fetch_article")
def test_show_all_articles_no_article(mock_fetch_article, mock_fetch_categories, capsys):
    """Test showing all articles when an article is not found."""
    mock_fetch_categories.return_value = ["positive", "science"]
    mock_fetch_article.return_value = None

    show_all_articles()

    captured = capsys.readouterr()
    assert "No article found for category" in captured.out
    mock_fetch_categories.assert_called_once()
    assert mock_fetch_article.call_count == 2


@patch("oneread.cli.fetch_categories")
def test_list_command(mock_fetch_categories, runner):
    """Test the list command."""
    mock_fetch_categories.return_value = ["positive", "science"]

    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "positive" in result.output
    assert "science" in result.output


@patch("oneread.cli.show_all_articles")
def test_default_command(mock_show_all, runner):
    """Test the default command (no arguments)."""
    result = runner.invoke(cli)
    assert result.exit_code == 0
    mock_show_all.assert_called_once()


@patch("oneread.cli.read_category_article")
def test_category_command(mock_read_category, runner):
    """Test reading a specific category."""
    result = runner.invoke(cli, ["positive"])
    assert result.exit_code == 0
    mock_read_category.assert_called_once_with("positive")


def test_help_command(runner):
    """Test the help command."""
    result = runner.invoke(cli, ["help"])
    assert result.exit_code == 0
    assert "OneRead" in result.output
    assert "Available commands" in result.output


@patch("oneread.cli.display_article")
@patch("oneread.cli.fetch_article")
def test_read_category_article(mock_fetch_article, mock_display_article, mock_article_content):
    """Test reading a category article."""
    mock_fetch_article.return_value = mock_article_content

    read_category_article("positive")

    mock_fetch_article.assert_called_once_with("positive")
    mock_display_article.assert_called_once_with(mock_article_content, "positive")


@patch("oneread.cli.fetch_article")
def test_category_not_found(mock_fetch_article, runner):
    """Test reading a category that doesn't exist."""
    mock_fetch_article.return_value = None

    result = runner.invoke(cli, ["nonexistent"])
    assert result.exit_code == 0
    assert "No article found for category" in result.output


@patch("oneread.cli.cli")
def test_main_exception_handling(mock_cli):
    """Test exception handling in the main function."""
    mock_cli.side_effect = Exception("Test error")

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert excinfo.value.code == 1


def test_main_execution():
    """Test the main function execution."""
    # We can't easily test the actual execution without running the CLI,
    # but we can at least import and call the function
    from oneread.cli import main

    # Just make sure it's callable
    assert callable(main)


def test_main_module_as_script():
    """Test running the cli module as a script."""
    import subprocess
    import sys

    import oneread

    # Get the path to the cli.py file
    cli_path = os.path.join(os.path.dirname(oneread.__file__), "cli.py")

    # Run the module as a script with coverage
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", "--append", cli_path],
        capture_output=True,
        text=True,
        check=False,
    )

    # Check that it ran successfully
    assert result.returncode == 0, f"Script failed with: {result.stderr}"
