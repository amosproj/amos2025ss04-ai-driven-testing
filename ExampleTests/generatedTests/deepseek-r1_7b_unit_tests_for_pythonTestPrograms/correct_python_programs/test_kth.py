import unittest

from correct_python_programs.kthfromcorrect_python_programs import kth
from correct_python_programsfromcorrect_python_programs import random


def kth(arr, k):
    pivot = arr[0]
    below = [x for x in arr if x < pivot]
    above = [x for x in arr if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if k < num_less:
        return kth(below, k)
    elif k >= num_lessoreq:
        return kth(above, k - num_lessoreq)
    else:
        return pivot


class TestKth(unittest.TestCase):
    @classmethod
    def test_kth(cls):
        # Test case 1: Simple sorted array with k=0 (should return first element)
        arr = [3, 6, 8]
        cls.assertEqual(kth(arr, 0), 3)

    @classmethod
    def test_kth_2(cls):
        # Test case 2: All elements are the same
        arr = [5] * 10
        expected = 5
        try:
            result = kth(arr, 4)
            assert result == expected
        except IndexError:
            print("List index out of range error")
            unittest.fail()

    @classmethod
    def test_kth_3(cls):
        # Test case 3: k equals number of elements below pivot
        arr = [2, 5, 7, 8]
        cls.assertEqual(kth(arr, num_less), 5)

    @classmethod
    def test_kth_4(cls):
        # Test case 4: Edge case where k is at the boundary between below and above
        arr = [1, 3, 5, 6, 7]
        expected = 5
        try:
            result = kth(arr, num_lessoreq)
            assert result == expected
        except IndexError as e:
            print("Index error occurred:", str(e))
            unittest.fail()


if __name__ == "__main__":
    unittest.main()
