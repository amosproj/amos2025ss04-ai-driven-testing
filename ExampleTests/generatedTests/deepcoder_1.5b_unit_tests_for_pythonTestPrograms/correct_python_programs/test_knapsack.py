import unittest
from collections import defaultdict


def knapsack(capacity, items):
    memo = defaultdict(int)

    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]

        for j in range(1, capacity + 1):
            memo[i, j] = memo[i - 1, j]

            if weight <= j:
                memo[i, j] = max(memo[i, j], value + memo[i - 1, j - weight])

    return memo[len(items), capacity]


class TestKnapsack(unittest.TestCase):
    def test_knapsack_zero_capacity(self):
        self.assertEqual(knapsack(0, [(5, 10)]), 0)

    def test_knapsack_single_item(self):
        items = [(2, 3)]
        self.assertEqual(knapsack(3, items), 3)

    def test_knapsack_different_items(self):
        items = [(1, 5), (2, 8)]
        capacity = 4
        expected = max(knapsack(4, items), knapsack(4, [(2, 8), (1, 5)]))
        self.assertEqual(knapsack(4, items), expected)

    def test_knapsack_negative_value(self):
        items = [(3, -5)]
        capacity = 0
        self.assertEqual(knapsack(capacity, items), -5)


if __name__ == "__main__":
    unittest.main()
