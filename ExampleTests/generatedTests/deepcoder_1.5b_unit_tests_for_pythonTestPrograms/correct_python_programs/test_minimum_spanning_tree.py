import unittest
from collections import defaultdict

def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=lambda x: x.__getitem__):
        u, v = edge
        if group_by_node.setdefault(u, {u}) != group_by_node.setdefault(v, {v}):
            mst_edges.add(edge)
            group_by_node[u].update(group_by_node[v])
            for node in group_by_node[v]:
                group_by_node[node] = group_by_node[u]

    return mst_edges

class Testminimum_spanning_tree(unittest.TestCase):

    def test_minimal_mst_with_same_nodes(self):
        # Create a graph where all edges are between node 0 and others
        weight_by_edge = {
            (0,1): {'a': 'a1', 'b': 'b1'},
            (0,2): {'a': 'a2', 'b': 'b2'},
            (1,2): {'a': 'a3', 'b': 'b3'}
        }
        expected_edges = {(0,1), (0,2)}
        result_edges = minimum_spanning_tree(weight_by_edge)
        self.assertEqual(expected_edges, result_edges)

    def test_minimal_mst_withdifferent_nodes(self):
        # Create a graph with two separate edges
        weight_by_edge = {
            (0,1): {'a': 'a1', 'b': 'b1'},
            (2,3): {'a': 'a2', 'b': 'b2'}
        }
        expected_edges = {(0,1), (2,3)}
        result_edges = minimum_spanning_tree(weight_by_edge)
        self.assertEqual(expected_edges, result_edges)

    def test_minimal_mst_single_node(self):
        # Create a graph with only one node
        weight_by_edge = {
            (0,0): {'a': 'a1'}
        }
        expected_edges = set()
        result_edges = minimum_spanning_tree(weight_by_edge)
        self.assertEqual(expected_edges, result_edges)

if __name__ == '__main__':
    unittest.main()