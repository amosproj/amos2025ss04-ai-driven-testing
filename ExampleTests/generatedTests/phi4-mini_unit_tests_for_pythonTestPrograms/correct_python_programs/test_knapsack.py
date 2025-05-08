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


import unittest


class TestKnapsack(unittest.TestCase):
    def test_empty_items(self):
        items = []
        self.assertEqual(knapsack(0, items), 0)

    def test_single_item_with_capacity_larger_than_weight_and_value(self):
        items = [(10, 60)]
        max_val_1 = knapsack(15, items)
        self.assertEqual(
            max_val_1, 60
        )  # Max value we can carry is the item's own value

    def test_multiple_items_all_fit_in_one_at_a_time(self):
        capacity = 7
        weights_values = [(4, 10), (5, 40)]
        max_value_single_passes = knapsack(
            capacity, [weights for weight in weights_values]
        )
        self.assertEqual(
            max_value_single_passes, sum(v for w, v in weights_values)
        )  # Assuming greedy approach

    def test_multiple_items_all_fit_together(self):
        capacity = 10
        items_to_pack = [(1, 6), (2, 7)]
        max_val_full_combination = knapsack(
            capacity, [weights for weight, value in zip(*items_to_pack)]
        )
        self.assertEqual(
            max_val_full_combination, sum(value for value, _ in items_to_pack)
        )  # Assuming greedy approach

    def test_items_that_do_not_fit_together(self):
        capacity = 10
        weights_values = [(1, 6), (3, 20)]
        max_value_no_packing_needed = knapsack(
            capacity, [weights for weight, value in zip(*weights_values)]
        )
        self.assertEqual(
            max_val_no_packing_needed,
            sum(value for value, _ in weights_values),
        )  # Assuming greedy approach

    def test_empty_capacity(self):
        capacity = 0
        items_with_zero_weight_value_1 = [(0, 10)]
        max_val_for_single_item = knapsack(
            capacity,
            [
                weights
                for weight, value in zip(*items_with_zero_weight_value_1)
            ],
        )
        self.assertEqual(
            max_val_for_single_item, sum(value for _, value in weights)
        )

    def test_maximum_capacity(self):
        capacity = 50
        items = [(10, 60), (20, 100)]
        max_value_two_items_packed_separately = knapsack(
            capacity, [weights for weight, value in zip(*items)]
        )
        self.assertEqual(
            max_val_two_items_packed_separately,
            sum(value for _, value in weights),
        )


if __name__ == "__main__":
    unittest.main()
