def wrap(text, cols):
    lines = []
    while len(text) > cols:
        end = text.rfind(' ', 0, cols + 1)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)
    lines.append(text)
    return lines


import unittest

class TestWrap(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.wrap_func = wrap
        
    def test_wrap_basic(self):
        result = self.wrap_func("Hello world", 5)
        expected = ["Hello", "world"]
        self.assertEqual(result, expected)

    def test_wrap_empty_string(self):
        result = self.wrap_func("", 5)
        expected = []
        self.assertEqual(result, expected)

    def test_wrap_exact_fit(self):
        result = self.wrap_func("Perfect day", 10)
        expected = ["Perfect day"]
        self.assertEqual(result, expected)

    def test_wrap_odd_number_of_wraps(self):
        result = self.wrap_func("This is a text with many words to wrap over multiple lines", 8)
        expected = [
            "This is a text with many",
            "words to wrap over multiple",
            "lines"
        ]
        self.assertEqual(result, expected)

    def test_wrap_cols_zero(self):
        result = self.wrap_func("Test string", 0)
        expected = ["Test string"]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
```

This TestWrap class provides:
1. Basic functionality testing
2. Empty string handling
3. Exact fit scenarios
4. Odd number of wrap cases
5. Column width of zero

The test methods are all annotated with `@classmethod` to be run against the class itself. The tests verify different edge cases and typical use cases for your wrap function.

To run the tests, simply execute the script, which will automatically discover and run all the test cases.

```bash
python -m unittest test_wrap.py