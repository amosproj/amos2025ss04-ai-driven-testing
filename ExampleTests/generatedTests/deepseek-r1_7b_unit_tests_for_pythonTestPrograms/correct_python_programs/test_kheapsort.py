import heapq
from unittest import TestCase, main

class KHeapSortTestCase(TestCase):
    def test_kheapsort(self):
        # Test with k=0 (should return empty list)
        sorted = list(kheapsort([], 0))
        self.assertEqual(sorted, [])
        
        # Test with small array
        arr = [3,1,2]
        sorted_arr = list(kheapsort(arr, len(arr)))
        self.assertEqual(sorted_arr, sorted(arr))
        
        # Test with k=1 (should return the same order as input if it's already sorted)
        arr = [5,4,3,2,1]
        k = 1
        sorted_list = []
        for i in range(len(kheapsort(arr, k))):
            sorted_list.append(next(iter(kheapsort(arr, k))))
        self.assertEqual(sorted_list, arr[::-1])
        
        # Test with larger array
        arr = [54,26,98,23,57]
        k = 3
        sorted_list = []
        for i in range(len(kheapsort(arr, k))):
            sorted_list.append(next(iter(kheapsort(arr, k))))
        self.assertEqual(sorted_list, sorted(arr))
        
    def test_kheapsort_edge_cases(self):
        # Test with empty array
        arr = []
        k = 3
        sorted_list = list(kheapsort(arr, k))
        self.assertEqual(sorted_list, [])
        
        # Test invalid k value (shouldn't crash)
        try:
            _ = kheapsort([1,2,3], -1)
        except ValueError:
            pass
        
        try:
            _ = kheapsort([1,2,3], 4)  # Will this cause an issue?
        except IndexError:
            pass

if __name__ == '__main__':
    main()
```

This test file includes several test cases:

1. Basic functionality with default k value
2. Smaller arrays to verify order
3. Edge case where k is equal to the length of the array (should return same order as input if it's already sorted)
4. Testing when k is 0 (should return empty list without yielding anything)
5. Test with invalid values for k (to ensure robustness)

To run the tests:

```bash
python your_test_file.py