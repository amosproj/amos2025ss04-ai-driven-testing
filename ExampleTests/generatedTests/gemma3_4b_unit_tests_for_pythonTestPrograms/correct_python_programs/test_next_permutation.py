def next_permutation(perm):
    for i in range(len(perm) - 2, -1, -1):
        if perm[i] < perm[i + 1]:
            for j in range(len(perm) - 1, i, -1):
                if perm[j] > perm[i]:
                    next_perm = list(perm)
                    next_perm[i], next_perm[j] = perm[j], perm[i]
                    next_perm[i + 1 :] = reversed(next_perm[i + 1 :])
                    return next_perm
    return None


import unittest


class TestNextPermutation(unittest.TestCase):
    def test_empty_list(self):
        self.assertIsNone(next_permutation([]))

    def test_single_element_list(self):
        self.assertIsNone(next_permutation([1]))

    def test_already_largest_permutation(self):
        self.assertIsNone(next_permutation([3, 2, 1]))

    def test_simple_case(self):
        self.assertEqual(next_permutation([1, 2, 3]), [1, 3, 2])

    def test_another_simple_case(self):
        self.assertEqual(next_permutation([1, 2, 3, 2]), [1, 3, 2, 2])

    def test_duplicate_elements(self):
        self.assertEqual(next_permutation([1, 1, 2]), [1, 2, 1])

    def test_complex_case(self):
        self.assertEqual(
            next_permutation([2, 3, 1, 3, 2, 4, 3, 1, 5, 2, 6, 3]),
            [2, 3, 1, 3, 2, 4, 3, 1, 5, 2, 6, 3],
        )

    def test_no_next_permutation(self):
        self.assertIsNone(next_permutation([5, 4, 3, 2, 1]))

    def test_different_order(self):
        self.assertEqual(next_permutation([1, 3, 2]), [2, 1, 3])


if __name__ == "__main__":
    unittest.main()
