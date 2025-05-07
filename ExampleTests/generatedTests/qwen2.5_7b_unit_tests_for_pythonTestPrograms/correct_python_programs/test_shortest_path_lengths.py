from collections import defaultdict


def shortest_path_lengths(n, length_by_edge):
    length_by_path = defaultdict(lambda: float('inf'))
    length_by_path.update({(i, i): 0 for i in range(n)})
    length_by_path.update(length_by_edge)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                length_by_path[i, j] = min(
                    length_by_path[i, j],
                    length_by_path[i, k] + length_by_path[k, j]
                )

    return length_by_path


import unittest
from collections import defaultdict


class TestShortestPathLengths(unittest.TestCase):

    def test_shortest_path_lengths(self):
        n = 3
        length_by_edge = {(0, 1): 2, (1, 2): 4, (0, 2): 6}
        expected_result = {
            (0, 0): 0, (0, 1): 2, (0, 2): 3,
            (1, 0): 2, (1, 1): 0, (1, 2): 4,
            (2, 0): 3, (2, 1): 4, (2, 2): 0
        }
        result = shortest_path_lengths(n, length_by_edge)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
```

To run the test:
```sh
python -m unittest <filename>