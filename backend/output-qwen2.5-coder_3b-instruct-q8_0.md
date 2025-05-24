To write unit tests for the `Graph` class using Python's `unittest` library, we need to cover various scenarios, including edge cases and typical use cases. Below is a set of test cases that cover different aspects of the `Graph` class:

```python
import unittest
from typing import Dict, List, Set

class TestGraph(unittest.TestCase):
    def setUp(self):
        # Define some test edges
        self.edges = [
            (1, 2), (2, 3), (3, 4), (4, 1),
            (2, 4), (1, 3)
        ]
        
        # Create a graph instance with the test edges
        self.graph = Graph(self.edges)

    def test_make_graph(self):
        # Check if the adjacency list is correctly built
        self.assertEqual(len(self.graph.graph), 4)
        for node in [1, 2, 3, 4]:
            self.assertIn(node, self.graph.graph)
            self.assertEqual(len(self.graph.graph[node]), 2)

    def test_visit_and_unvisit(self):
        # Test visiting and unvisiting a node
        start = 1
        self.graph.visit(start)
        self.assertTrue(self.graph.visited[start])
        self.assertFalse(self.graph.un_visit(start))

    def test_all_nodes_are_visited(self):
        # Check if all nodes are visited after a path
        self.graph.get_hamiltonian_path(1)
        self.assertTrue(self.graph.all_nodes_are_visited())

    def test_get_hamiltonian_path(self):
        # Test the basic Hamiltonian path finding functionality
        hamiltonian_paths = self.graph.get_hamiltonian_path(start=1)
        expected_paths = [
            [1, 2, 4, 3, 1],
            [1, 3, 4, 2, 1]
        ]
        self.assertIn(hamiltonian_paths[0], expected_paths)
        self.assertIn(hamiltonian_paths[1], expected_paths)

    def test_invalid_start(self):
        # Test an invalid start node
        with self.assertRaises(ValueError) as context:
            self.graph.get_hamiltonian_path(start=5)
        self.assertEqual(str(context.exception), "Start node 5 is not in the graph")

    def test_empty_graph(self):
        # Test a graph with no edges
        empty_edges = []
        empty_graph = Graph(empty_edges)
        expected_paths = []
        
        with self.assertRaises(ValueError) as context:
            empty_graph.get_hamiltonian_path(start=1)
        self.assertEqual(str(context.exception), "Graph is empty")

if __name__ == "__main__":
    unittest.main()
```

### Explanation:

- **`setUp` Method**: This method initializes a `Graph` instance with a set of test edges. It's called before each test method to ensure the graph state is consistent.

- **`test_make_graph`**: This test checks if the adjacency list is correctly constructed and contains the expected number of nodes and connections.

- **`test_visit_and_unvisit`**: This test verifies that the `visit` and `un_visit` methods work as intended by checking the state of a node after visiting and unvisiting it.

- **`test_all_nodes_are_visited`**: This test checks if the graph correctly identifies when all nodes have been visited during path construction.

- **`test_get_hamiltonian_path`**: This test verifies that the `get_hamiltonian_path` method returns the expected Hamiltonian paths for a simple graph. It also includes an expected list of paths for validation.

- **`test_invalid_start`**: This test checks if the method raises an appropriate error when an invalid start node is provided.

- **`test_empty_graph`**: This test checks if the method raises an appropriate error when the graph is empty (i.e., no edges).

These tests should cover a wide range of scenarios and ensure that the `Graph` class behaves as expected.