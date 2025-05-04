import unittest

def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        if group_by_node.setdefault(u, {u}) != group_by_node.setdefault(v, {v}):
            mst_edges.add(edge)
            group_by_node[u].update(group_by_node[v])
            for node in group_by_node[v]:
                group_by_node[node] = group_by_node[u]

    return mst_edges


class TestMinimumSpanningTree(unittest.TestCase):

    def test_empty_graph(self):
        weight_by_edge = {}
        expected_mst_edges = set()
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected_mst_edges)

    def test_single_node(self):
        weight_by_edge = {}
        expected_mst_edges = set()
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected_mst_edges)

    def test_two_nodes_one_edge(self):
        weight_by_edge = {
            (0, 1): 1
        }
        expected_mst_edges = {(0, 1)}
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected_mst_edges)

    def test_two_nodes_multiple_edges(self):
        weight_by_edge = {
            (0, 1): 1,
            (1, 2): 2,
            (0, 2): 3
        }
        expected_mst_edges = {(0, 1), (1, 2)}
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected_mst_edges)

    def test_complex_graph(self):
        weight_by_edge = {
            (0, 1): 4,
            (0, 2): 8,
            (1, 2): 11,
            (1, 3): 8,
            (2, 3): 7,
            (0, 4): 9,
            (1, 3): 14,
            (2, 5): 10,
            (3, 4): 5,
            (3, 5): 6,
            (4, 5): 3
        }
        expected_mst_edges = {(4, 5), (0, 1), (2, 3), (0, 4), (1, 3), (2, 5)}
        self.assertEqual(minimum_spanning_tree(weight_by_edge), expected_mst_edges)


if __name__ == '__main__':
    unittest.main()