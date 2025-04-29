import heapq
import unittest

def kheapsort(arr, k):
    import heapq

    heap = arr[:k]
    heapq.heapify(heap)

    for x in arr[k:]:
        yield heapq.heappushpop(heap, x)

    while heap:
        yield heapq.heappop(heap)

class TestKheapsort(unittest.TestCase):

    def test_empty_array(self):
        self.assertEqual(list(kheapsort([], 0)), [])
        self.assertEqual(list(kheapsort([], 5)), [])

    def test_k_equals_0(self):
        arr = [5, 1, 4, 2, 8]
        self.assertEqual(list(kheapsort(arr, 0)), arr)

    def test_k_equals_array_length(self):
        arr = [5, 1, 4, 2, 8]
        expected = sorted(arr)
        actual = list(kheapsort(arr, len(arr)))
        self.assertEqual(actual, expected)

    def test_k_less_than_array_length(self):
        arr = [5, 1, 4, 2, 8]
        k = 3
        expected = sorted(arr[:k] + arr[k:])
        actual = list(kheapsort(arr, k))
        self.assertEqual(actual, expected)

    def test_k_greater_than_array_length(self):
        arr = [5, 1, 4, 2, 8]
        k = 10
        expected = sorted(arr)
        actual = list(kheapsort(arr, k))
        self.assertEqual(actual, expected)

    def test_duplicate_elements(self):
        arr = [5, 1, 4, 2, 8, 1, 4]
        k = 3
        expected = sorted(arr[:k] + arr[k:])
        actual = list(kheapsort(arr, k))
        self.assertEqual(actual, expected)
    
    def test_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        k = 3
        expected = sorted(arr[:k] + arr[k:])
        actual = list(kheapsort(arr, k))
        self.assertEqual(actual, expected)
    
    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        k = 3
        expected = sorted(arr[:k] + arr[k:])
        actual = list(kheapsort(arr, k))
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()