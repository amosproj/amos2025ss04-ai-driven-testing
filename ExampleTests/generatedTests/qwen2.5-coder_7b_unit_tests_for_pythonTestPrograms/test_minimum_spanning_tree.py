import unittest


def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        if group_by_node.setdefault(u, {u}) != group_by_node.setdefault(
            v, {v}
        ):
            mst_edges.add(edge)
            group_by_node[u].update(group_by_node[v])
            for node in group_by_node[v]:
                group_by_node[node] = group_by_node[u]

    return mst_edges


class TestMinimumSpanningTree(unittest.TestCase):
    def test_minimum_spanning_tree(self):
        weight_by_edge = {("A", "B"): 1, ("B", "C"): 2, ("A", "C"): 4}
        expected_result = {("A", "B"), ("B", "C")}
        result = minimum_spanning_tree(weight_by_edge)
        self.assertEqual(result, expected_result)

    def test_minimum_spanning_tree_with_multiple_edges(self):
        weight_by_edge = {
            ("A", "B"): 1,
            ("B", "C"): 2,
            ("A", "C"): 3,
            ("C", "D"): 4,
            ("B", "D"): 5,
        }
        expected_result = {("A", "B"), ("B", "C"), ("C", "D")}
        result = minimum_spanning_tree(weight_by_edge)
        self.assertEqual(result, expected_result)

    def test_minimum_spanning_tree_with_self_loop(self):
        weight_by_edge = {("A", "B"): 1, ("B", "B"): 2, ("A", "C"): 4}
        expected_result = {("A", "B")}
        result = minimum_spanning_tree(weight_by_edge)
        self.assertEqual(result, expected_result)

    def test_minimum_spanning_tree_with_no_edges(self):
        weight_by_edge = {}
        expected_result = set()
        result = minimum_spanning_tree(weight_by_edge)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
