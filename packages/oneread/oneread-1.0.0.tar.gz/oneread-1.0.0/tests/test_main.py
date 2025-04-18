"""Tests for the OneRead __main__ module."""

import os
import subprocess
import sys
from unittest.mock import patch


def test_main_module_structure():
    """Test the structure of the __main__.py file."""
    # Get the path to the __main__.py file
    import oneread
    main_path = os.path.join(os.path.dirname(oneread.__file__), "__main__.py")

    # Read the file content
    with open(main_path, 'r') as f:
        content = f.read()

    # Check that it imports the main function
    assert "from oneread.cli import main" in content

    # Check that it has the if __name__ == "__main__" block
    assert 'if __name__ == "__main__":' in content

    # Check that it calls main() inside the if block
    assert "main()" in content


@patch("oneread.cli.main")
def test_main_module_execution(mock_main):
    """Test executing the __main__ module."""
    # Import the module directly
    from oneread import __main__

    # Call the code that would be executed if run as __main__
    __main__._main_function_for_testing()

    # Verify main was called
    mock_main.assert_called_once()


def test_main_module_as_script():
    """Test running the __main__ module as a script."""
    import oneread

    # Get the path to the __main__.py file
    main_path = os.path.join(os.path.dirname(oneread.__file__), "__main__.py")

    # Run the module as a script with coverage
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", "--append", main_path],
        capture_output=True,
        text=True,
        check=False,
    )

    # Check that it ran successfully
    assert result.returncode == 0, f"Script failed with: {result.stderr}"
