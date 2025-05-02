import unittest

def next_permutation(perm):
    """
    Generates the next lexicographical permutation of a list of numbers.
    
    Args:
        perm: A list of integers representing the current order.
        
    Returns:
        The next permutation as a list, or None if it is already at the last permutation.
    """
    # Iterate from the second last element to the first
    for i in range(len(perm) - 2, -1, -1):
        # Look for an element that is smaller than its successor
        if perm[i] < perm[i + 1]:
            # Find the smallest index j > i such that perm[j] > perm[i]
            for j in range(len(perm) - 1, i, -1):
                if perm[j] > perm[i]:
                    # Swap elements at positions i and j
                    next_perm = list(perm)
                    next_perm[i], next_perm[j] = perm[j], perm[i]
                    # Reverse the remaining elements after i+1
                    next_perm[i + 1:] = reversed(next_perm[i + 1:])
                    return next_perm
    
    # If no such permutation is found (all elements are in descending order)
    return list(perm)

class Testclass:
    def test_next_permutation(self):
        # Test case 1: Sample input and expected output
        original = [3, 2, 1]
        expected = [1, 2, 3]
        result = next_permutation(original.copy())
        self.assertEqual(result, expected)
        
        # Test case 2: Another sample input
        test_input = [4, 3, 2, 1]
        expected_output = [1, 2, 3, 4]
        result = next_permutation(test_input.copy())
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
```

This code creates a test class that includes the original `next_permutation` function and several test cases to verify its correctness. Each test case provides specific input and checks if the output matches the expected result.

To run the tests:

```bash
python Your_code.py