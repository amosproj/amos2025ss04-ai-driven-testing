import unittest


def levenshtein(source, target):
    if source == "" or target == "":
        return len(source) or len(target)

    elif source[0] == target[0]:
        return levenshtein(source[1:], target[1:])

    else:
        return 1 + min(
            levenshtein(source, target[1:]),
            levenshtein(source[1:], target[1:]),
            levenshtein(source[1:], target),
        )


class TestLevenshtein(unittest.TestCase):
    def test_empty_strings(self):
        self.assertEqual(levenshtein("", ""), 0)
        self.assertEqual(levenshtein("a", ""), 1)
        self.assertEqual(levenshtein("", "b"), 1)

    def test_single_character_matches(self):
        self.assertEqual(levenshtein("a", "a"), 0)
        self.assertEqual(levenshtein("ab", "ab"), 0)

    def test_single_character_mismatches(self):
        self.assertEqual(levenshtein("a", "b"), 1)
        self.assertEqual(levenshtein("abc", "abd"), 1)

    def test_multiple_character_cases(self):
        self.assertEqual(levenshtein("kitten", "sitting"), 3)
        self.assertEqual(levenshtein("flaw", "lawn"), 2)


if __name__ == "__main__":
    unittest.main()
