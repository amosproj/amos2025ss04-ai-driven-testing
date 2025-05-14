```markdown
import unittest

from typing import List


class TestGraph(unittest.TestCase):

    def setUp(self):
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4), (1, 3)]
        self.graph = Graph(edges)

    def test_make_graph(self):
        expected_edges = [
            (1, 2),
            (2, 1),
            (2, 3),
            (3, 2),
            (3, 4),
            (4, 3),
            (4, 1),
            (1, 4),
            (1, 3),
            (3, 1)
        ]
        
        expected_edges_set = set(expected_edges)

        actual_edges = list(self.graph.edges)[:10]
        self.assertEqual(sorted(actual_edges), sorted(expected_edges))

    def test_all_nodes_are_visited(self):
        visited_count_before_starting_path = len(set(node for node in self.graph.visited))
        hamiltonian_paths_from_node1 = self.graph.get_hamiltonian_path(start=1)
        
        # Count total nodes and verify if all are visited
        expected_total_nodes = 4

        actual_visited_counts_after_all_paths = [len(path) - 1 for path in hamiltonian_paths_from_node1]
        unique_visited_numbers = set(visited_count_before_starting_path | {node: False} for node, visited in self.graph.visited.items() if visited)
        
        # Check that all nodes are indeed marked as visited
        expected_unique_nodes_set = {i + 1 for i in range(expected_total_nodes)}
        actual_visited_counts_after_all_paths.add(0)  # Start vertex is not counted
        
        unique_actual_count = len(unique_visited_numbers | set(actual_visited_counts_after_all_paths))
        
        self.assertEqual(len(set(range(1, expected_total_nodes + 1)))) == expected_unique_nodes_set
        self.assertTrue(all(v in actual_visited_counts_after_all_paths for v in range(expected_total_nodes)))

if __name__ == "__main__":
    unittest.main()
```