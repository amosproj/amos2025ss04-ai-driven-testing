"""Module for finding the first occurrence of an element in a sorted array.

This module provides a binary search-based function to efficiently locate
the first occurrence of a specified value in a sorted array.
"""


def find_first_in_sorted(arr, x):
    """Find the index of the first occurrence of a value in a sorted array.

    Uses a modified binary search algorithm to find the first occurrence
    of a specified value in a sorted array with O(log n) time complexity.

    Args:
        arr: A sorted list of comparable elements
        x: The value to search for

    Returns:
        int: The index of the first occurrence of x in arr,
             or -1 if x is not found in the array
    """
    lo = 0
    hi = len(arr)

    while lo < hi:
        mid = (lo + hi) // 2

        if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
            return mid

        elif x <= arr[mid]:
            hi = mid

        else:
            lo = mid + 1

    return -1
