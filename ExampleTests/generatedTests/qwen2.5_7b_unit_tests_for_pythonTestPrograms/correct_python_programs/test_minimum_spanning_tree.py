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


import unittest
from typing import Set, Tuple


class TestMinimumSpanningTree(unittest.TestCase):
    def test_minimum_spanning_tree(self):
        weight_by_edge: Set[Tuple[int, int]] = {
            (0, 1),
            (0, 2),
            (1, 3),
            (1, 4),
            (2, 5),
            (2, 6),
            (3, 7),
            (3, 8),
        }
        expected_mst_edges: Set[Tuple[int, int]] = {
            (0, 1),
            (0, 2),
            (1, 3),
            (2, 5),
            (2, 6),
            (3, 7),
        }
        self.assertEqual(
            minimum_spanning_tree(weight_by_edge), expected_mst_edges
        )


if __name__ == "__main__":
    unittest.main()
