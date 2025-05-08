import unittest


def shortest_paths(source, weight_by_edge):
    weight_by_node = {v: float("inf") for u, v in weight_by_edge}
    weight_by_node[source] = 0

    for _ in range(
        len(weight_by_node) - 1
    ):  # Changed to len instead of fixed range (len-1)
        for (u, v), weight in weight_by_edge.items():
            if weight_by_node[u] + weight < weight_by_node[v]:
                weight_by_node[v] = weight_by_node[u] + weight

    return weight_by_node


class TestShortestPaths(unittest.TestCase):
    def test_shortest_paths(self):
        graph1 = {("A", "B"): 1, ("B", "C"): 2}
        source = "A"
        expected_output = {"A": 0, "B": 1, "C": 3}

        result = shortest_paths(source, graph1)

        self.assertEqual(result["A"], expected_output["A"])
        self.assertEqual(result["B"], expected_output["B"])
        self.assertEqual(result["C"], expected_output["C"])

    def test_empty_graph(self):
        source = "A"
        empty_graph = {}

        result = shortest_paths(source, empty_graph)

        # In an infinite graph case we can safely return the initial weights
        self.assertTrue(
            all(weight == float("inf") for weight in result.values())
        )

    def test_single_node(graph):
        single_node = {("A", "B"): 1}
        source = "A"
        expected_output = {"A": 0}

        graph.update(single_node)

        result = shortest_paths(source, graph)

        self.assertEqual(result["A"], expected_output["A"])

    def test_no_edge(self):
        source = "A"
        no_edges_graph = {}

        # Expect all weights to be infinity since there are no edges
        results = shortest_paths(source, no_edges_graph)

        for key in [
            "B",
            "C",
        ]:  # Assuming B and C exist as nodes but not connected.
            self.assertEqual(results[key], float("inf"))


if __name__ == "__main__":
    unittest.main()
