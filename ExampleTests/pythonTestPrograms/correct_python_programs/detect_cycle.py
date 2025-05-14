"""Module for detecting cycles in linked lists using Floyd's algorithm.

This module provides a function to detect if a linked list contains
a cycle using the "tortoise and hare" approach, also known as
Floyd's cycle-finding algorithm.
"""


def detect_cycle(node):
    """Detect if a linked list contains a cycle.

    Uses Floyd's cycle-finding algorithm (also known as the "tortoise and hare"
    algorithm) to efficiently detect cycles in a linked list with O(n) time
    complexity and O(1) space complexity.

    Args:
        node: The head node of the linked list to check

    Returns:
        bool: True if the linked list contains a cycle, False otherwise
    """
    hare = tortoise = node

    while True:
        if hare is None or hare.successor is None:
            return False

        tortoise = tortoise.successor
        hare = hare.successor.successor

        if hare is tortoise:
            return True
