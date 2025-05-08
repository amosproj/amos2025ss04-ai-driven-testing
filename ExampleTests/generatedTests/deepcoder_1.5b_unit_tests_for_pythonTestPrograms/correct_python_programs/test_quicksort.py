import unittest

from correct_python_programs.quicksort import quicksort


def quicksort(arr):
    if not arr:
        return []

    pivot = arr[0]
    lesser = quicksort([x for x in arr[1:] if x < pivot])
    greater = quicksort([x for x in arr[1:] if x >= pivot])
    return lesser + [pivot] + greater


def test_quicksort_empty_list():
    input_list = []
    result = quicksort(input_list)
    assert input_list == result, "Test should pass when input is empty."

def test_quicksort_single_element():
    input_list = [5]
    result = quicksort(input_list)
    assert input_list == result, "Test should pass when input has one element."

def test_quicksort_sorted_list():
    input_list = [3, 1, 2]
    result = quicksort(input_list)
    assert result == input_list, "Test should pass for sorted list."

class Testclass(unittest.TestCase):
    def __init__(self):
        self.setup()

    def setup(self):
        self.input_arr = []

def test_quicksort_empty_list_test():
    test Case: input is empty
    input_list = []
    result = quicksort(input_list)
    assert input_list == result, "Test should pass when input is empty."

def test_quicksort_single_element_test():
    input_list = [5]
    result = quicksort(input_list)
    assert input_list == result, "Test should pass when input has one element."

def test_quicksort_sorted_list_test():
    input_list = [3, 1, 2]
    result = quicksort(input_list)
    assert result == input_list, "Test should pass for sorted list."

# Create Testclass instance
test_case = Testclass()

if __name__ == "__main__":
    unittest.main()