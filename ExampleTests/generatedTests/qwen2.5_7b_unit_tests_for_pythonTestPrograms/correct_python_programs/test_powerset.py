def powerset(arr):
    if arr:
        first, *rest = arr
        rest_subsets = powerset(rest)
        return [[first] + subset for subset in rest_subsets] + rest_subsets
    else:
        return [[]]

import unittest

class TestPowerset(unittest.TestCase):

    def test_powerset(self):
        self.assertEqual(powerset([1, 2, 3]), 
                         [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []])

    def test_empty_array(self):
        self.assertEqual(powerset([]), [[]])

    def test_single_element(self):
        self.assertEqual(powerset([1]), [[1], []])

if __name__ == '__main__':
    unittest.main()
```

To create a runnable file, you can save the above code in a Python script and run it. For example:

```python
def powerset(arr):
    if arr:
        first, *rest = arr
        rest_subsets = powerset(rest)
        return [[first] + subset for subset in rest_subsets] + rest_subsets
    else:
        return [[]]

import unittest

class TestPowerset(unittest.TestCase):

    def test_powerset(self):
        self.assertEqual(powerset([1, 2, 3]), 
                         [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []])

    def test_empty_array(self):
        self.assertEqual(powerset([]), [[]])

    def test_single_element(self):
        self.assertEqual(powerset([1]), [[1], []])

if __name__ == '__main__':
    unittest.main()