"""Test module for the hello_world functionality.

This module contains tests for the hello_world function to ensure
it correctly outputs the expected greeting message.
"""


def hello_world():
    """Print a simple greeting message to the console.

    This function demonstrates the basic functionality being tested
    and outputs "Hello, World!" to standard output.

    Returns:
        None
    """
    print("Hello, World!")


def test_hello_world(capfd):
    """Test that the hello_world function outputs the correct message.

    This test verifies that the hello_world function properly prints
    the "Hello, World!" message to standard output.

    Args:
        capfd: Pytest fixture to capture stdout/stderr output

    Assertions:
        The function should output exactly "Hello, World!" followed by a newline
    """
    hello_world()
    captured = capfd.readouterr()
    assert captured.out == "Hello, World!\n"
