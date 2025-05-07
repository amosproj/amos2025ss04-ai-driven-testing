import unittest


class TestFindFirstInSorted(unittest.TestCase):
    def test_find_first_in_sorted(self):
        arr = [1, 2, 4, 4, 6]
        self.assertEqual(find_first_in_sorted(arr, 4), 2)

        arr = [1, 2, 3, 4, 5, 6]
        self.assertEqual(find_first_in_sorted(arr, 7), -1)

        arr = [2, 2, 2, 2, 2]
        self.assertEqual(find_first_in_sorted(arr, 2), 0)

        arr = [1]
        self.assertEqual(find_first_in_sorted(arr, 1), 0)

        arr = []
        self.assertEqual(find_first_in_sorted(arr, 1), -1)


if __name__ == "__main__":
    unittest.main()
