import unittest


def knapsack(capacity, items):
    from collections import defaultdict

    memo = defaultdict(int)

    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]

        for j in range(1, capacity + 1):
            memo[i, j] = memo[i - 1, j]

            if weight <= j:
                memo[i, j] = max(memo[i, j], value + memo[i - 1, j - weight])

    return memo[len(items), capacity]


class TestKnapsack(unittest.TestCase):
    def test_empty_items(self):
        self.assertEqual(knapsack(10, []), 0)

    def test_single_item_fits(self):
        items = [(5, 10)]
        self.assertEqual(knapsack(10, items), 10)

    def test_single_item_does_not_fit(self):
        items = [(15, 10)]
        self.assertEqual(knapsack(10, items), 0)

    def test_multiple_items_fit(self):
        items = [(5, 10), (4, 40), (6, 30), (3, 50)]
        self.assertEqual(knapsack(10, items), 90)

    def test_multiple_items_dont_fit(self):
        items = [(5, 10), (4, 40), (6, 30), (3, 50)]
        self.assertEqual(knapsack(5, items), 50)

    def test_zero_capacity(self):
        items = [(5, 10), (4, 40), (6, 30), (3, 50)]
        self.assertEqual(knapsack(0, items), 0)

    def test_large_capacity(self):
        items = [(1, 1), (2, 3), (3, 4), (5, 6)]
        self.assertEqual(knapsack(10, items), 10)


if __name__ == "__main__":
    unittest.main()
