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


if __name__ == "__main__":
    import unittest

    class TestLevenshtein(unittest.TestCase):
        def test_empty_strings(self):
            self.assertEqual(levenshtein("", ""), 0)
            self.assertEqual(levenshtein("abc", ""), 3)
            self.assertEqual(levenshtein("", "def"), 3)

        def test_identical_strings(self):
            self.assertEqual(levenshtein("abc", "abc"), 0)
            self.assertEqual(levenshtein("hello", "hello"), 0)

        def test_single_substitution(self):
            self.assertEqual(levenshtein("abc", "abd"), 1)
            self.assertEqual(levenshtein("kitten", "sitting"), 3)

        def test_multiple_substitutions(self):
            self.assertEqual(levenshtein("intention", "execution"), 5)
            self.assertEqual(levenshtein("ros", "rose"), 1)

        def test_insertions_and_deletions(self):
            self.assertEqual(levenshtein("abc", "axc"), 1)
            self.assertEqual(levenshtein("ab", "abcde"), 1)

        def test_long_strings(self):
            self.assertEqual(
                levenshtein("thisisalongstring", "thisisalongstring"), 0
            )
            self.assertEqual(levenshtein("abcdefgh", "bcdefgh"), 1)

    def main():
        unittest.main()

    if __name__ == "__main__":
        main()
