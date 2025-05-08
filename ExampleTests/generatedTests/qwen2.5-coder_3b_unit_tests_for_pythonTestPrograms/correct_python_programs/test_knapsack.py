import unittest


class TestKnapsack(unittest.TestCase):
    def test_knapsack(self):
        # Test case 1: Simple test case with weights and values
        items = [(2, 3), (3, 4), (5, 7)]
        capacity = 6
        expected_result = 8
        self.assertEqual(knapsack(capacity, items), expected_result)

        # Test case 2: Larger capacity with more items
        items = [(10, 100), (20, 150), (30, 200)]
        capacity = 50
        expected_result = 350
        self.assertEqual(knapsack(capacity, items), expected_result)

        # Test case 3: No items in the list
        items = []
        capacity = 10
        expected_result = 0
        self.assertEqual(knapsack(capacity, items), expected_result)

        # Test case 4: Capacity is greater than all item weights
        items = [(5, 20)]
        capacity = 10
        expected_result = 20
        self.assertEqual(knapsack(capacity, items), expected_result)

        # Test case 5: Weight of an item exceeds the capacity
        items = [(6, 30)]
        capacity = 5
        expected_result = 0
        self.assertEqual(knapsack(capacity, items), expected_result)


if __name__ == "__main__":
    unittest.main()
