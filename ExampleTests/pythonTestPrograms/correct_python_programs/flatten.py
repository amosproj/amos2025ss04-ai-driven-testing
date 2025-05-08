"""Module for flattening nested arrays.

This module provides a generator function to recursively flatten
nested lists into a single-level sequence of elements.
"""


def flatten(arr):
    """Convert a nested list structure into a flat sequence.

    Recursively traverses the input, yielding each non-list element
    encountered while unpacking nested lists. The function preserves
    the order of elements as they appear in the original structure.

    Args:
        arr: A list potentially containing nested lists

    Yields:
        Elements from the nested structure in depth-first order
    """
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x
