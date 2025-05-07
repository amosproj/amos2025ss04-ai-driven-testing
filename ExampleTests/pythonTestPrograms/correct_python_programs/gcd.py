"""Module for calculating the greatest common divisor (GCD).

This module implements Euclid's algorithm to efficiently find the largest
positive integer that divides both input numbers without a remainder.
"""


def gcd(a, b):
    """Calculate the greatest common divisor of two integers.

    Uses Euclid's algorithm, which states that if a = bq + r, then
    gcd(a, b) = gcd(b, r), with the base case gcd(a, 0) = a.

    Args:
        a: First integer
        b: Second integer

    Returns:
        int: The greatest common divisor of a and b
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
