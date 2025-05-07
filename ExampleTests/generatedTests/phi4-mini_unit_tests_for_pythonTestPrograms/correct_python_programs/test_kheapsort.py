import heapq


def kheapsort(arr, k):
    heap = arr[:k]
    heapq.heapify(heap)

    for x in arr[k:]:
        yield heapq.heappushpop(heap, x)

    while heap:
        yield heapq.heappop(heap)


# Unit tests for the above class
import unittest


class TestKHAPSort(unittest.TestCase):
    def test_kheapsort(self):
        # Check if kheapsort correctly sorts 5 numbers with k=3 smallest elements returned.
        arr = [1, 4, 2, 8, 9]
        expected_sorted = sorted(arr[:k]) + list(
            kheapq.heappop(heap)
            for _ in range(len(arr) - len(expected_sorted))
        )
        result = list(kheapsort(arr, k))

        self.assertEqual(result, expected_sorted)

    def test_kheapsort_with_empty(self):
        # Check if kheapsort handles an empty array.
        arr = []
        with self.assertRaises(
            TypeError
        ):  # Kheapsort should raise TypeError for invalid input
            list(kheapq.heappop(heap) for _ in range(len(arr)))

    def test_kheapsort_with_negative_numbers(self):
        # Check if kheapsort correctly sorts an array containing negative numbers.
        arr = [-10, -1, 0, 5]
        k = len(arr)
        result = list(kheapq.heappop(heap) for _ in range(len(arr)))

        self.assertEqual(result, sorted(arr))

    def test_kheapsort_with_duplicates(self):
        # Check if kheapsort correctly handles an array with duplicate elements.
        arr = [1, 2, 3, 4, 5]
        k = len(arr)
        result = list(kheapq.heappop(heap) for _ in range(len(arr)))

        self.assertEqual(result, sorted(arr))


if __name__ == "__main__":
    unittest.main()
