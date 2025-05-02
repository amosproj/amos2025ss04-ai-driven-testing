import unittest

def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start == end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid + 1, end)
        else:
            return mid

    return binsearch(0, len(arr))

class TestFindInSorted(unittest.TestCase):
    def setUp(self):
        self.test_array = [5, 7, 9]
    
    def test_find_in_sorted_middle(self):
        # Test case: looking for middle element
        arr = [5, 7, 9]
        x = 7
        expected_index = 1
        result = find_in_sorted(arr, x)
        
        self.assertEqual(expected_index, result)
    
    def test_find_in_sorted_higher(self):
        # Test case: looking for a number higher than all elements
        arr = [5, 7, 9]
        x = 10
        expected_result = -1
        result = find_in_sorted(arr, x)
        
        self.assertEqual(expected_result, result)
    
    def test_find_in_sorted_not_present_start(self):
        # Test case: looking for a number not present at start position
        arr = [5, 7, 9]
        x = 5
        expected_index = 0
        result = find_in_sorted(arr, x)
        
        self.assertEqual(expected_index, result)
    
    def test_find_in_sorted_not_present_mid_plus_one(self):
    # Test case: looking for a number not present at mid+1 position
        arr = [5, 7, 9]
        x = 6
        expected_result = -1
        result = find_in_sorted(arr, x)
        
        self.assertEqual(expected_result, result)
    
    def test_find_in_sorted_not_present_end(self):
        # Test case: looking for a number not present at end position
        arr = [5, 7, 9]
        x = 10
        expected_result = -1
        result = find_in_sorted(arr, x)
        
        self.assertEqual(expected_result, result)

    def test_empty_array(self):
        # Test case: empty array
        arr = []
        x = 3
        expected_result = -1
        result = find_in_sorted(arr, x)
        
        self.assertEqual(expected_result, result)
    
    def test_single_element_array(self):
        # Test case: single element array
        arr = [4]
        x = 4
        expected_index = 0
        result = find_in_sorted(arr, x)
        
        self.assertEqual(expected_index, result)

if __name__ == '__main__':
    unittest.main()
```

This test file:
1. Defines a `TestFindInSorted` class inheriting from `unittest.TestCase`
2. Creates a `setUp()` method to initialize test fixtures
3. Contains several test methods for different cases:
   - Looking for middle element (should return correct index)
   - Looking for higher number than all elements (returns -1)  
   - Looking for numbers not present in array positions 0, mid+1, and end 
   - Tests edge cases: empty array and single-element array
4. Uses `unittest.main()` to run all tests when the script is executed

You can run these tests by running:
```bash
python your_test_file.py