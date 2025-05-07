import heapq
import unittest


def shortest_path_length(length_by_edge, startnode, goalnode):
    unvisited_nodes = []  # FibHeap containing (node, distance) pairs
    heappush(unvisited_nodes, (0, startnode))
    visited_nodes = set()

    while len(unvisited_nodes) > 0:
        distance, node = heappop(unvisited_nodes)
        if node is goalnode:
            return distance

        visited_nodes.add(node)

        for nextnode in node.successors:
            if nextnode in visited_nodes:
                continue

            insert_or_update(
                unvisited_nodes,
                (
                    min(
                        get(unvisited_nodes, nextnode) or float("inf"),
                        distance + length_by_edge[node, nextnode],
                    ),
                    nextnode,
                ),
            )

    return float("inf")


def get(node_heap, wanted_node):
    for dist, node in node_heap:
        if node == wanted_node:
            return dist
    return 0


def insert_or_update(node_heap, dist_node):
    dist, node = dist_node
    for i, tpl in enumerate(node_heap):
        a, b = tpl
        if b == node:
            node_heap[i] = dist_node  # heapq retains sorted property
            return None

    heappush(node_heap, dist_node)
    return None


class TestShortestPathLength(unittest.TestCase):
    def setUp(self):
        self.length_by_edge = {
            ("A", "B"): 1,
            ("A", "C"): 4,
            ("B", "D"): 2,
            ("C", "D"): 3,
        }
        self.successors_A = ["B", "C"]
        self.successors_B = ["D"]
        self.successors_C = []

    def test_shortest_path_length(self):
        node_A = {"successors": self.successors_A}
        node_B = {"successors": self.successors_B, "distance_from_A": 1}
        node_C = {}
        node_D = {}

        # Setting up graph edges with lengths
        self.length_by_edge["A", "B"] = 1
        self.length_by_edge["A", "C"] = 4
        self.length_by_edge["B", "D"] = 2
        self.length_by_edge["C", "D"] = 3

        # Test shortest path from A to D directly through B, which is shorter than C -> D.
        result = shortest_path_length(self.length_by_edge, node_A, node_D)
        self.assertEqual(
            result, float("inf")
        )  # No direct edge exists in this setup.

    def test_shortest_path_length_via_B(self):
        path_result_via_B = shortest_path_length(
            self.length_by_edge, {"successors": ["B"]}, "D"
        )
        expected_distance_via_B = (
            self.length_by_edge["A", "B"] + self.length_by_edge["B", "D"]
        )
        self.assertEqual(path_result_via_B, expected_distance_via_B)

    def test_shortest_path_length_via_C(self):
        path_result_via_C = shortest_path_length(
            self.length_by_edge, {"successors": ["C"]}, "D"
        )
        expected_distance_via_C = float(
            "inf"
        )  # No direct edge exists in this setup.


if __name__ == "__main__":
    unittest.main()
