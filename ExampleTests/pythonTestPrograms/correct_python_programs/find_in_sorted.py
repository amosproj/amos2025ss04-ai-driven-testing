"""Module for binary search implementation in a sorted array.

This module provides a function that performs a binary search to find
the index of a specific element in a sorted array.
"""


def find_in_sorted(arr, x):
    """Search for an element in a sorted array using binary search.

    Implements a recursive binary search algorithm to efficiently locate
    a specific value in a sorted array with O(log n) time complexity.

    Args:
        arr: A sorted list of comparable elements
        x: The value to search for

    Returns:
        int: The index of x in arr if found, or -1 if not present
    """

    def binsearch(start, end):
        if start == end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid + 1, end)
        else:
            return mid

    return binsearch(0, len(arr))
