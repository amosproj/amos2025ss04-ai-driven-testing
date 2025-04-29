def next_permutation(perm):
    for i in range(len(perm) - 2, -1, -1):
        if perm[i] < perm[i + 1]:
            for j in range(len(perm) - 1, i, -1):
                if perm[j] > perm[i]:
                    next_perm = list(perm)
                    next_perm[i], next_perm[j] = perm[j], perm[i]
                    next_perm[i + 1:] = reversed(next_perm[i + 1:])
                    return next_perm

import unittest
from itertools import permutations


class TestNextPermutation(unittest.TestCase):
    def test_next_permutation(self):
        self.assertEqual(next_permutation([1, 2, 3]), [1, 3, 2])
        self.assertEqual(next_permutation([3, 2, 1]), [1, 2, 3])
        self.assertEqual(next_permutation([1, 1, 5]), [1, 5, 1])
        self.assertEqual(next_permutation([1, 3, 2]), [2, 1, 3])
        self.assertEqual(next_permutation([4, 3, 2, 1]), [1, 2, 3, 4])
        self.assertEqual(next_permutation([1, 4, 5, 2, 3]), [1, 4, 5, 3, 2])


if __name__ == '__main__':
    unittest.main()