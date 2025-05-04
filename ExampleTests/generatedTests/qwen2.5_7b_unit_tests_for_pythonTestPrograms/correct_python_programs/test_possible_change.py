def possible_change(coins, total):
    if total == 0:
        return 1
    if not coins or total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

import unittest

class TestPossibleChange(unittest.TestCase):

    def test_possible_change(self):
        self.assertEqual(possible_change([1, 2, 5], 5), 4)
        self.assertEqual(possible_change([1, 2, 3], 4), 4)
        self.assertEqual(possible_change([1], 0), 1)
        self.assertEqual(possible_change([], 1), 0)
        self.assertEqual(possible_change([1, 2, 5], -1), 0)

if __name__ == '__main__':
    unittest.main()