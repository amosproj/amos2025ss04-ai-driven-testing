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


import unittest

class TestLevenshteinDistance(unittest.TestCase):
    def test_empty_strings(self):
        self.assertEqual(levenshtein('', ''), 0)

    def test_single_char_strings(self):
        self.assertEqual(levenshtein('a', 'b'), 1)
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('', 'a'), 1)

    def test_simple_examples(self):
        self.assertEqual(levenshtein('kitten', 'sitting'), 3)
        self.assertEqual(levenshtein('Saturday', 'Sunday'), 3)
        self.assertEqual(levenshtein('professor', 'prospero'), 2)

    def test_self_distance(self):
        for s in ['a', 'abcde', 'hello world']:
            self.assertEqual(levenshtein(s, s), 0)


if __name__ == '__main__':
    unittest.main()