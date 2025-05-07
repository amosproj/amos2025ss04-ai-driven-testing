import unittest
from heapq import heapify, heappushpop, heappop


def kheapsort(arr, k):
    import heapq

    heap = arr[:k]
    heapq.heapify(heap)

    for x in arr[k:]:
        yield heappushpop(heap, x)

    while heap:
        yield heappop(heap)


class TestKHeapsort(unittest.TestCase):
    def test_kheapsort_small_array(self):
        self.assertEqual(list(kheapsort([1, 2, 3], 2)), [1, 2, 3])

    def test_kheapsort_with_duplicates(self):
        self.assertEqual(
            list(kheapsort([5, 7, 4, 7, 9, 6, 5], 3)), [4, 5, 5, 6, 7, 7, 9]
        )

    def test_kheapsort_empty_array(self):
        self.assertEqual(list(kheapsort([], 0)), [])

    def test_kheapsort_with_one_element(self):
        self.assertEqual(list(kheapsort([42], 1)), [42])

    def test_kheapsort_with_large_k(self):
        arr = list(range(100))
        self.assertEqual(list(kheapsort(arr, 50)), sorted(arr))


if __name__ == "__main__":
    unittest.main()
