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

class TestShortestPathLengths(unittest.TestCase):

    def test_empty_graph(self):
        n = 3
        length_by_edge = {}
        expected = {}
        result = shortest_path_lengths(n, length_by_edge)
        self.assertEqual(result, expected)

    def test_simple_graph(self):
        n = 3
        length_by_edge = {(0, 1): 1, (1, 2): 2, (0, 2): 5}
        expected = {
            (0, 0): 0,
            (0, 1): 1,
            (0, 2): 6,
            (1, 0): 1,
            (1, 1): 0,
            (1, 2): 2,
            (2, 0): 5,
            (2, 1): 2,
            (2, 2): 0
        }
        result = shortest_path_lengths(n, length_by_edge)
        self.assertEqual(result, expected)

    def test_disconnected_graph(self):
        n = 4
        length_by_edge = {(0, 1): 1, (2, 3): 2}
        expected = {
            (0, 0): 0,
            (0, 1): 1,
            (0, 2): float('inf'),
            (0, 3): float('inf'),
            (1, 0): 1,
            (1, 1): 0,
            (1, 2): float('inf'),
            (1, 3): float('inf'),
            (2, 0): float('inf'),
            (2, 1): float('inf'),
            (2, 2): 0,
            (2, 3): 2,
            (3, 0): float('inf'),
            (3, 1): float('inf'),
            (3, 3): 0
        }
        result = shortest_path_lengths(n, length_by_edge)
        self.assertEqual(result, expected)

    def test_single_node(self):
        n = 1
        length_by_edge = {}
        expected = {(0, 0): 0}
        result = shortest_path_lengths(n, length_by_edge)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()