"""Implementation of the bubble sort algorithm.

This module provides a function to sort a list using the bubble sort algorithm,
which repeatedly steps through the list, compares adjacent elements, and swaps
them if they are in the wrong order. The algorithm is demonstrated with a
sample list at the end of the module.
"""


def bubble_sort(arr):
    """Sort a list using the bubble sort algorithm.

    This implementation includes an optimization that stops the algorithm
    when no swaps are needed, indicating that the list is already sorted.

    Args:
        arr: The list to be sorted (modified in-place)

    Returns:
        None: The input list is modified in-place
    """
    for n in range(len(arr) - 1, 0, -1):
        swapped = False
        for i in range(n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break


# Sample list to be sorted
arr = [6, 6, 2]
print("Unsorted list is:")
print(arr)

bubble_sort(arr)

print("Sorted list is:")
print(arr)
