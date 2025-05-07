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
    def test_empty_graph(self):
        self.assertEqual(minimum_spanning_tree(set()), set())

    def test_single_edge(self):
        weight_map = {(1, 2): 10}
        result = minimum_spanning_tree(weight_map)
        expected_edges = {(1, 2)}
        self.assertTrue(result.issubset(expected_edges))

    def test_two_nodes_with_one_edge(self):
        weight_map = {(1, 2): 5}
        mst_result = set()
        for edge in sorted(weight_map.keys(), key=lambda x: weight_map[x]):
            u, v = edge
            if not group_by_node.setdefault(
                u, {u}
            ) == group_by_node.setdefault(v, {v}):
                mst_edges.add(edge)
                group_by_node[u].update(group_by_node[v])
        expected_mst_result = {(1, 2)}
        self.assertTrue(mst_result.issubset(expected_mst_result))

    def test_multiple_edges(self):
        weight_map = {(1, 2): 5, (3, 4): 10}
        mst_result = set()
        for edge in sorted(weight_map.keys(), key=lambda x: weight_map[x]):
            u, v = edge
            if not group_by_node.setdefault(
                u, {u}
            ) == group_by_node.setdefault(v, {v}):
                mst_edges.add(edge)
                group_by_node[u].update(group_by_node[v])
        expected_mst_result = {(1, 2), (3, 4)}
        self.assertTrue(mst_result.issubset(expected_mst_result))

    def test_complex_graph(self):
        weight_map = {(1, 2): 5, (1, 3): 6, (2, 3): 7}
        mst_edges_set = minimum_spanning_tree(weight_map)
        expected_mst_edges_set = {(1, 2), (1, 3)}

        # Check if the MST contains all edges from our expectation
        self.assertTrue(mst_edges_set == set(expected_mst_edges_set))


if __name__ == "__main__":
    unittest.main()
