"""Module for counting the number of set bits in an integer.

This module provides a function to determine the number of 1s in the binary
representation of an integer using the Brian Kernighan's algorithm.
"""


def bitcount(n):
    """Count the number of set bits (1s) in the binary representation of an integer.

    This implementation uses Brian Kernighan's algorithm, which has time complexity
    proportional to the number of 1s in the binary representation.

    Args:
        n: A non-negative integer

    Returns:
        int: The number of 1s in the binary representation of n
    """
    count = 0
    while n:
        n &= n - 1  # Clear the least significant bit set to 1
        count += 1
    return count
