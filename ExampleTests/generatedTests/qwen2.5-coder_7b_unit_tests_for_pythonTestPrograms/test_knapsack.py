import unittest

def knapsack(capacity, items):
    from collections import defaultdict
    memo = defaultdict(int)

    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]

        for j in range(1, capacity + 1):
            memo[i, j] = memo[i - 1, j]

            if weight <= j:
                memo[i, j] = max(
                    memo[i, j],
                    value + memo[i - 1, j - weight]
                )

    return memo[len(items), capacity]


class TestKnapsack(unittest.TestCase):
    def test_knapsack(self):
        self.assertEqual(knapsack(50, [(10, 60), (20, 100), (30, 120)]), 220)
        self.assertEqual(knapsack(10, [(2, 4), (3, 7)]), 7)
        self.assertEqual(knapsack(5, [(2, 3), (3, 4)]), 4)
        self.assertEqual(knapsack(100, [(20, 60), (30, 100), (40, 120)]), 220)

if __name__ == '__main__':
    unittest.main()