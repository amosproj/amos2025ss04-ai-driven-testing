import unittest

from correct_python_programs.pascalfromcorrect_python_programsfromcorrect_python_programsfromcorrect_python_programsfromcorrect_python_programs import \
    pascal


class Testclass(unittest.TestCase):
    def __init__(self):
        self.test_cases = [
            (1, [[1]]),
            (2, [[1], [1, 1]]),
            (3, [[1], [1, 1], [1, 2, 1]])
        ]

    def test(self, n, expected):
        rows = pascal(n)
        for actual, expected in zip(rows, expected):
            self asserts that actual equals expected

if __name__ == '__main__':
    unittest.main()
```

```python
import unittest

from correct_python_programs.pascalfromcorrect_python_programsfromcorrect_python_programsfromcorrect_python_programsfromcorrect_python_programs import \
    pascal


class Testclass(unittest.TestCase):
    def __init__(self):
        self.test_cases = [
            (1, [[1]]),
            (2, [[1], [1, 1]]),
            (3, [[1], [1, 1], [1, 2, 1]])
        ]

    def test(self, n, expected):
        rows = pascal(n)
        for actual, expected in zip(rows, expected):
            self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()