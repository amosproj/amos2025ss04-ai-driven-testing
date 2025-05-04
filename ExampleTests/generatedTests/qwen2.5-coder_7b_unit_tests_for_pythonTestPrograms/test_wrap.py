import unittest

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

class TestWrap(unittest.TestCase):
    def test_wrap_single_line(self):
        result = wrap("HelloWorld", 5)
        expected = ["Hello", "World"]
        self.assertEqual(result, expected)

    def test_wrap_multiple_lines(self):
        result = wrap("This is a long sentence that should be wrapped", 10)
        expected = ["This is a", "long", "sentence", "that", "should", "be", "wrapped"]
        self.assertEqual(result, expected)

    def test_wrap_at_space(self):
        result = wrap("Split this line at space", 6)
        expected = ["Split", "this", "line", "at", "space"]
        self.assertEqual(result, expected)

    def test_wrap_no_spaces(self):
        result = wrap("Nospaceshere", 5)
        expected = ["No", "spaces", "here"]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()