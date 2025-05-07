import unittest


def levenshtein(source, target):
    if source == "" or target == "":
        return len(source) + len(target)

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

    def test_one_string(self):
        source = "abc"
        expected_length_difference = len("b") + len("c")
        result_diff1 = levenshtein(source, "")
        result_diff2 = levenshtein("", source)

        self.assertEqual(
            result_diff1, expected_length_difference * 3
        )  # each character in the first string contributes to three length differences
        self.assertEqual(result_diff2, expected_length_difference * 3)

    def test_empty_target(self):
        target = ""
        for char in "abc":
            result = levenshtein(char, "")
            self.assertEqual(
                result, len("a" + chr(ord(char) - ord("a")))
            )  # calculate the length difference dynamically based on previous characters

    def test_one_char_difference(self):
        source = "abcd"
        target = "abef"  # only one character change
        expected_diff_count = 1

        result_length_differences = [
            levenshtein(source, t) for t in ("abcdef", "abcdeg")
        ]

        self.assertEqual(
            result_length_differences[0], len("abcd") + len("abcdefgh")
        )
        self.assertLessEqual(result_length_differences[1], expected_diff_count)

    def test_multiple_characters_difference(self):
        source = "abcde"
        target = "abfgh"  # two characters change
        expected_diff_count_approximation = len(source) - 2 + len(target)

        result_lengths = [
            levenshtein("abcdef", "abfg"),
            levenshtein("abcdefg", "abcdefgh"),
        ]
        self.assertEqual(result_lengths, sorted([len("abcd"), len("abcde")]))


if __name__ == "__main__":
    unittest.main()
