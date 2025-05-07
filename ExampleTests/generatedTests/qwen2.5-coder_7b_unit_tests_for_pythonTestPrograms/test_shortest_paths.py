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
    def test_shortest_paths_basic(self):
        source = "A"
        weight_by_edge = {("A", "B"): 1, ("B", "C"): 2, ("A", "C"): 4}
        expected_result = {"A": 0, "B": 1, "C": 3}
        self.assertEqual(
            shortest_paths(source, weight_by_edge), expected_result
        )

    def test_shortest_paths_disconnected(self):
        source = "A"
        weight_by_edge = {("A", "B"): 1, ("B", "C"): 2, ("D", "E"): 3}
        expected_result = {
            "A": 0,
            "B": 1,
            "C": 3,
            "D": float("inf"),
            "E": float("inf"),
        }
        self.assertEqual(
            shortest_paths(source, weight_by_edge), expected_result
        )

    def test_shortest_paths_negative_weight(self):
        source = "A"
        weight_by_edge = {("A", "B"): -1, ("B", "C"): 2}
        with self.assertRaises(ValueError):
            shortest_paths(source, weight_by_edge)


if __name__ == "__main__":
    unittest.main()
