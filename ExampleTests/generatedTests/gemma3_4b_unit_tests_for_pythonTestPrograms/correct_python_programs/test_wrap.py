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


if __name__ == '__main__':
    import unittest

    class TestWrap(unittest.TestCase):

        def test_empty_string(self):
            self.assertEqual(wrap("", 10), [""])

        def test_single_word(self):
            self.assertEqual(wrap("hello", 3), ["hello"])

        def test_multiple_words(self):
            self.assertEqual(wrap("hello world", 3), ["hello", "world"])

        def test_long_string(self):
            text = "This is a very long string that needs to be wrapped to multiple lines."
            expected = ["This is a", "very long", "string that", "needs to be", "wrapped to", "multiple lines."]
            self.assertEqual(wrap(text, 10), expected)

        def test_wrap_with_spaces(self):
            text = "hello   world  this   is  a   test"
            expected = ["hello", "world", "this", "is", "a", "test"]
            self.assertEqual(wrap(text, 3), expected)

        def test_wrap_with_long_word(self):
            text = "abcdefghijklmnopqrstuvwxyz"
            expected = ["abcdefgh", "ijklmnop", "qrstuvwx", "yz"]
            self.assertEqual(wrap(text, 5), expected)

    if __name__ == '__main__':
        unittest.main()