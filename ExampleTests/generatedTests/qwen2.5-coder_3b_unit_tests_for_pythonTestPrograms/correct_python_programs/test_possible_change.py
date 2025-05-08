import unittest


class TestPossibleChange(unittest.TestCase):
    def test_possible_change(self):
        self.assertEqual(possible_change([1, 2, 5], 5), 4)
        self.assertEqual(possible_change([1, 2, 5], 6), 7)
        self.assertEqual(possible_change([1, 2, 5], 7), 13)
        self.assertEqual(possible_change([1, 2, 5], 8), 24)
        self.assertEqual(possible_change([1, 2, 5], 9), 44)
        self.assertEqual(possible_change([], 0), 1)
        self.assertEqual(possible_change([1], -1), 0)
        self.assertEqual(possible_change([2], 3), 1)
        self.assertEqual(possible_change([3], 6), 2)


if __name__ == "__main__":
    unittest.main()
