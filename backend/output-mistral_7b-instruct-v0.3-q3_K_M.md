 Here is a simple implementation of unit tests using the `unittest` library in Python for the provided `Graph` class. This test suite checks if the `get_hamiltonian_path()` method correctly identifies Hamiltonian paths and if it handles unvisited nodes properly.

```python
import unittest
from your_module import Graph

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph([(1, 2), (2, 3), (3, 4), (4, 1), (2, 4), (1, 3)])

    def test_get_hamiltonian_path(self):
        hamiltonian_paths = self.graph.get_hamiltonian_path(start=1)
        expected_paths = [ [1, 2, 4, 3], [1, 2, 3, 4] ]
        for path in hamiltonian_paths:
            self.assertListEqual(path, expected_paths[len(hamiltonian_paths) - 1])
            expected_paths.pop()

    def test_visited_nodes(self):
        graph = Graph([(1, 2), (2, 3), (3, 4), (4, 5)])
        with self.assertRaises(AssertionError):
            graph.get_hamiltonian_path(start=1)
        graph.visit(1)
        graph.get_hamiltonian_path(start=1)
        self.assertEqual(graph.visited_nodes, 5)
        graph.un_visit(1)
        graph.get_hamiltonian_path(start=2)
        self.assertEqual(graph.visited_nodes, 4)

if __name__ == "__main__":
    unittest.main()
```

In the provided test suite:

- The `test_get_hamiltonian_path()` checks that the `get_hamiltonian_path()` method correctly identifies Hamiltonian paths starting from the given node in a specific graph.
- The `test_visited_nodes()` function tests if the `Graph` class correctly counts visited nodes during recursive calls to the `get_hamiltonian_path()` function.