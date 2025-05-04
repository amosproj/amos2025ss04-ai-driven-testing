import unittest
from max_sublist_sum import max_sublist_sum

class Testclass:
    def test_max_sublist_sum(self):
        arr = [1, 2, 3]
        self.assertEqual(max_sublist_sum(arr), 6)

        arr = [-1, -2, -3]
        self.assertEqual(max_sublist_sum(arr), -6)

        arr = []
        self.assertEqual(max_sublist_sum(arr), 0)

        arr = [7, -8, 3]
        self.assertEqual(max_sublist_sum(arr), 9)

if __name__ == '__main__':
    unittest.main()