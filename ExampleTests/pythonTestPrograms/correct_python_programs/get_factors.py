"""Module for calculating prime factors of integers.

This module provides a function to find the prime factorization of a given
integer using trial division with optimization to check divisors only up to
the square root of the number.
"""


def get_factors(n):
    """Calculate the prime factorization of a positive integer.

    Uses a recursive algorithm that finds the smallest factor of the number,
    then recursively finds the prime factorization of the quotient.

    Args:
        n: A positive integer greater than 1

    Returns:
        list: A list of the prime factors of n in non-decreasing order
    """
    if n == 1:
        return []

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return [i] + get_factors(n // i)

    return [n]
