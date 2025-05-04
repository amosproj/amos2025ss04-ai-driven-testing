import unittest

def possible_change(coins, total):
    if total == 0:
        return 1
    if total < 0 or not coins:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

class TestPossibleChange(unittest.TestCase):

    def test_empty_coins(self):
        self.assertEqual(possible_change([], 5), 0)

    def test_zero_total(self):
        self.assertEqual(possible_change([1, 2, 5], 0), 1)

    def test_positive_change(self):
        self.assertEqual(possible_change([1, 2, 5], 5), 1)
        self.assertEqual(possible_change([1, 2, 5], 7), 1)
        self.assertEqual(possible_change([1, 2, 5], 10), 1)

    def test_negative_total(self):
        self.assertEqual(possible_change([1, 2, 5], -1), 0)

    def test_coin_not_in_solution(self):
        self.assertEqual(possible_change([2, 5], 3), 0)

    def test_multiple_coins(self):
        self.assertEqual(possible_change([1, 2, 5], 10), 1)
        self.assertEqual(possible_change([1, 2, 5], 12), 1)

    def test_large_total(self):
        self.assertEqual(possible_change([1, 2, 5], 20), 1)

    def test_complex_case(self):
        self.assertEqual(possible_change([1,5,10,25], 30), 4)

if __name__ == '__main__':
    unittest.main()