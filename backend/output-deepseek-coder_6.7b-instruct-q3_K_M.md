```python
import unittest
from yourfile import Graph  # replace with the actual module name

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph([(1,2), (2,3), (3,4), (4,1), (2,4), (1,3)])
        
    def test_init(self):
        self.assertEqual(len(self.graph.edges), 6)
        self.assertEqual(len(self.graph.graph.keys()), 4)
    
    def test_visit(self):
        self.assertFalse(self.graph.visited[1])
        self.graph.visit(1)
        self.assertTrue(self.graph.visited[1])
        
    def test_un_visit(self):
        self.graph.visit(2)
        self.assertEqual(self.graph.visited_nodes, 1)
        self.graph.un_visit(2)
        self.assertFalse(self.graph.visited[2])
        
    def test_all_nodes_are_visited(self):
        # initially all nodes should be unvisited
        self.assertFalse(self.graph.all_nodes_are_visited())
        for node in self.graph.graph.keys():
            self.graph.visit(node)
        self.assertTrue(self.graph.all_nodes_are_visited())
        
    def test_get_hamiltonian_path(self):
        paths = self.graph.get_hamiltonian_path(1)
        # for the given graph, there should be 2 possible Hamiltonian paths starting from node 1
        self.assertEqual(len(paths), 2)
        
if __name__ == "__main__":
    unittest.main()
```
This unit test file contains tests to check the functionality of `Graph` class methods like `visit`, `un_visit`, `all_nodes_are_visited` and `get_hamiltonian_path`. 
The `setUp` method is used to create a graph for testing with some predefined edges. The test cases are created to check if the methods return expected values or not. The tests are run by calling unittest's main function at the end of this file, which will discover and run all tests automatically.
