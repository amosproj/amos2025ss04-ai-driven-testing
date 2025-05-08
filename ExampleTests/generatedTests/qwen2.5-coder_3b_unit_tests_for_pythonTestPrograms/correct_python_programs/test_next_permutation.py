import unittest


class TestNextPermutation(unittest.TestCase):
    def test_next_permutation(self):
        # Test case 1: Basic permutation
        self.assertEqual(next_permutation([3, 2, 1]), [1, 2, 3])

        # Test case 2: Single element permutation
        self.assertEqual(next_permutation([5]), [5])

        # Test case 3: Already maximal permutation
        self.assertEqual(next_permutation([1, 2, 3]), [3, 1, 2])

        # Test case 4: Simple increasing order
        self.assertEqual(next_permutation([1, 3, 2]), [2, 1, 3])

        # Test case 5: Inversion at the end
        self.assertEqual(next_permutation([1, 2, 4, 3]), [1, 2, 3, 4])

        # Test case 6: Inversion in the middle
        self.assertEqual(next_permutation([1, 4, 3, 2]), [2, 1, 3, 4])

        # Test case 7: Large permutation with multiple inversions
        self.assertEqual(
            next_permutation([9, 8, 7, 6, 5, 4, 3, 2, 1]),
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        )


if __name__ == "__main__":
    unittest.main()
