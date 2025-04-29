import unittest

def levenshtein(source, target):
    if source == '' or target == '':
        return len(source) or len(target)

    elif source[0] == target[0]:
        return levenshtein(source[1:], target[1:])

    else:
        return 1 + min(
            levenshtein(source,     target[1:]),
            levenshtein(source[1:], target[1:]),
            levenshtein(source[1:], target)
        )

class TestLevenshtein(unittest.TestCase):

    def test_empty_strings(self):
        self.assertEqual(levenshtein('', ''), 0)

    def test_source_empty(self):
        self.assertEqual(levenshtein('', 'abc'), 3)

    def test_target_empty(self):
        self.assertEqual(levenshtein('abc', ''), 3)

    def test_equal_strings(self):
        self.assertEqual(levenshtein('abc', 'abc'), 0)

    def test_single_char_diff(self):
        self.assertEqual(levenshtein('a', 'b'), 1)

    def test_multiple_chars_diff(self):
        self.assertEqual(levenshtein('abc', 'axc'), 1)
        self.assertEqual(levenshtein('abc', 'abx'), 1)
        self.assertEqual(levenshtein('abc', 'acx'), 1)

if __name__ == '__main__':
    unittest.main()