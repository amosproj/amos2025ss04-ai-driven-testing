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
        # Test case 1: Simple graph with no redundant edges
        weight_by_edge = {("A", "B"): 1, ("B", "C"): 2, ("A", "C"): 3}
        expected = {("A", "B"), ("B", "C")}
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected)

        # Test case 2: Graph with redundant edges
        weight_by_edge = {("A", "B"): 1, ("A", "C"): 1, ("B", "C"): 2}
        expected = {("A", "B"), ("B", "C")}
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected)

        # Test case 3: Graph with isolated nodes
        weight_by_edge = {("A", "B"): 1, ("C", "D"): 2}
        expected = set()
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected)

        # Test case 4: Graph with one edge
        weight_by_edge = {("A", "B"): 5}
        expected = {("A", "B")}
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected)


if __name__ == "__main__":
    unittest.main()
