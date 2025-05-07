"""Implementation of bucket sort algorithm for integers.

This module provides a function to sort an array of integers within a known range
using the bucket sort algorithm, which has O(n+k) time complexity where n is the
array length and k is the range of values.
"""


def bucketsort(arr, k):
    """Sort an array of integers using the bucket sort algorithm.

    This implementation assumes all elements in the array are non-negative integers
    less than k. It counts occurrences of each number and rebuilds the sorted array.

    Args:
        arr: List of non-negative integers to be sorted
        k: Upper bound for the values in the array (exclusive)

    Returns:
        list: A new sorted list containing the same elements as the input array
    """
    counts = [0] * k
    for x in arr:
        counts[x] += 1

    sorted_arr = []
    for i, count in enumerate(counts):
        sorted_arr.extend([i] * count)

    return sorted_arr
