import unittest


def possible_change(coins, total):
    if total == 0:
        return 1
    if total < 0 or not coins:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)


class TestPossibleChange(unittest.TestCase):
    def test_total_zero(self):
        self.assertEqual(possible_change([1, 2, 3], 0), 1)

    def test_empty_coins(self):
        self.assertEqual(possible_change([], 5), 0)

    def test_negative_total(self):
        self.assertEqual(possible_change([1, 2, 3], -1), 0)

    def test_positive_total_with_coins(self):
        self.assertEqual(possible_change([1, 2, 3], 5), 4)

    def test_total_exceeds_sum_of_coins(self):
        self.assertEqual(possible_change([1, 2, 3], 10), 0)


if __name__ == "__main__":
    unittest.main()
