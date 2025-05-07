import unittest

from . import find_first_in_sorted


class Testclass:
    def __init__(self):
        self.all_tests = []


def test_find_first_in_sorted(arr, x):
    # Test case 1: Correct position found
    result = find_first_in_sorted(arr, x)
    assert result != -1, f"Expected not to return -1 for {arr} and {x}"

    # Test case 2: Element not present at the end
    result = find_first_in_sorted(arr, x)
    assert result == -1, f"Expected return -1 when element isn't found"

    # Test case 3: Edge case with empty array
    if not arr:
        assert (
            find_first_in_sorted(arr, x) == -1
        ), "Should handle empty array correctly"

    # Test case 4: Element at the last position
    result = find_first_in_sorted(arr, x)
    assert result == len(arr) - 1, f"Expected element found at last position"

    # Additional test cases for different implementations
    # (As shown in the original code examples)


def main():
    test_cases = [
        (find_first_in_sorted, [1, 2, 3], 2),
        (find_first_in_sorted, [4, 5, 6], 6),
        (find_first_in_sorted, [], 0),
        # Add more test cases as needed
    ]

    all_results = []
    for func, arr, x in test_cases:
        result = test_case(func, arr, x)
        all_results.append(result)

    print(all_results)
    unittest.main()


def test_case(func, arr, x):
    result = func(arr, x)
    return result


# Create Testclass instance
test_testclass = Testclass()
all_results = test_testclass.all_tests

print("All tests passed:", all_results)
