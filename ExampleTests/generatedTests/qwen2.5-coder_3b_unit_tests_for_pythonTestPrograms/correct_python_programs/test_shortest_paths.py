import unittest


def shortest_paths(source, weight_by_edge):
    weight_by_node = {v: float("inf") for u, v in weight_by_edge}
    weight_by_node[source] = 0

    for i in range(len(weight_by_node) - 1):
        for (u, v), weight in weight_by_edge.items():
            weight_by_node[v] = min(
                weight_by_node[u] + weight, weight_by_node[v]
            )

    return weight_by_node


class TestShortestPaths(unittest.TestCase):
    def test_shortest_paths(self):
        # Test case 1: Simple graph with positive weights
        weight_by_edge_1 = {(0, 1): 2, (0, 2): 4, (1, 2): 1, (1, 3): 5}
        source_node_1 = 0
        expected_output_1 = {0: 0, 1: 2, 2: 3, 3: 6}
        self.assertEqual(
            shortest_paths(source_node_1, weight_by_edge_1), expected_output_1
        )

        # Test case 2: Graph with negative weights
        weight_by_edge_2 = {(0, 1): -2, (0, 2): -4, (1, 2): 1, (1, 3): 5}
        source_node_2 = 0
        expected_output_2 = {0: 0, 1: -2, 2: -3, 3: -6}
        self.assertEqual(
            shortest_paths(source_node_2, weight_by_edge_2), expected_output_2
        )

        # Test case 3: Graph with negative cycle (should raise ValueError)
        weight_by_edge_3 = {(0, 1): -2, (1, 2): -4, (2, 0): 7}
        source_node_3 = 0
        self.assertRaises(
            ValueError, shortest_paths, source_node_3, weight_by_edge_3
        )


if __name__ == "__main__":
    unittest.main()
