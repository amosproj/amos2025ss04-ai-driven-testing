def shortest_paths(source, weight_by_edge):
    weight_by_node = {v: float("inf") for u, v in weight_by_edge}
    weight_by_node[source] = 0

    for i in range(len(weight_by_node) - 1):
        for (u, v), weight in weight_by_edge.items():
            weight_by_node[v] = min(
                weight_by_node[u] + weight, weight_by_node[v]
            )

    return weight_by_node


import unittest
from collections import defaultdict


class ShortestPathsTest(unittest.TestCase):
    def test_shortest_paths(self):
        # Test case 1: Simple graph with three nodes
        edges = {("A", "B"): 1, ("B", "C"): 2, ("A", "C"): 4}
        result = shortest_paths("A", edges)
        self.assertEqual(result, {"A": 0, "B": 1, "C": 3})

        # Test case 2: Graph with a negative cycle (will raise ValueError)
        try:
            edges_with_negative_cycle = {
                ("A", "B"): -1,
                ("B", "C"): 2,
                ("C", "A"): 1,
            }
            shortest_paths("A", edges_with_negative_cycle)
            self.fail("Expected a ValueError for negative cycle")
        except ValueError:
            pass

        # Test case 3: Graph with multiple paths to the same node (should take minimum path)
        edges_with_duplicates = {
            ("A", "B"): 1,
            ("C", "B"): -2,  # This should be ignored due to negative cycle
            ("D", "B"): 5,
            ("E", "F"): 3,
        }
        result = shortest_paths("A", edges_with_duplicates)
        self.assertEqual(
            result,
            {
                "A": 0,
                "B": 1,
                "C": float("inf"),
                "D": float("inf"),
                "E": float("inf"),
                "F": float("inf"),
            },
        )


if __name__ == "__main__":
    unittest.main()
