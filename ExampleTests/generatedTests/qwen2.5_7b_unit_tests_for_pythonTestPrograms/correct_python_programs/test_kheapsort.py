import heapq
from typing import Iterator
import unittest


def kheapsort(arr, k) -> Iterator[int]:
    heap = arr[:k]
    heapq.heapify(heap)

    for x in arr[k:]:
        yield heapq.heappushpop(heap, x)

    while heap:
        yield heapq.heappop(heap)


class TestKHeapsort(unittest.TestCase):
    def test_kheapsort(self) -> None:
        result: list[int] = []
        for value in kheapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0], 4):
            result.append(value)

        self.assertEqual(result, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_empty_array(self) -> None:
        result: list[int] = []
        for value in kheapsort([], 3):
            result.append(value)

        self.assertEqual(result, [])

    def test_k_greater_than_length(self) -> None:
        result: list[int] = []
        for value in kheapsort([5, 4, 3, 2, 1], 6):
            result.append(value)

        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_single_element(self) -> None:
        result: list[int] = []
        for value in kheapsort([7], 1):
            result.append(value)

        self.assertEqual(result, [7])


if __name__ == "__main__":
    unittest.main()
