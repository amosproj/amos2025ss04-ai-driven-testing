Here's an example of how you might test the Graph class using Python's unittest library. 

```python
import unittest
from yourfile import Graph  # replace 'yourfile' with the name of the file where this code is located

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph([(1,2), (2,3), (3,4), (4,1), (2,4), (1,3)])

    def test_make_graph(self):
        edges = [(5,6), (6,7)]
        self.graph.make_graph(edges)
        
        # check if new nodes are added to the graph
        for node in [5, 6, 7]:
            self.assertIn(node, self.graph.graph)
            
        # check if edges are correctly added
        self.assertSetEqual(self.graph.graph[5], {6})
        self.assertSetEqual(self.graph.graph[6], {5, 7})
        
    def test_visit(self):
        node = 1
        self.graph.visit(node)
        
        # check if the node is marked as visited
        self.assertEqual(self.graph.visited[node], True)
    
    def test_un_visit(self):
        node = 2
        self.graph.visit(node)  # mark node as visited first
        
        self.graph.un_visit(node)
        
        # check if the node is marked as unvisited (i.e., it's not in the visited set anymore)
        self.assertEqual(self.graph.visited[node], False)
    
    def test_all_nodes_are_visited(self):
        nodes = [1, 2]
        
        # mark all nodes as visited
        for node in nodes:
            self.graph.visit(node)
            
        self.assertEqual(self.graph.all_nodes_are_visited(), True)
    
    def test_get_hamiltonian_path(self):
        start = 1
        
        hamiltonian_paths = [[1,2], [1,4]]  # replace with the actual Hamiltonian paths in your graph
        
        self.assertEqual(self.graph.get_hamiltonian_path(start), hamiltonian_paths)

if __name__ == '__main__':
    unittest.main()
```

Please note that you need to replace the `yourfile` in `from yourfile import Graph` with the name of the file where this code is located, and define `hamiltonian_paths` in the test_get_hamiltonian_path method with the actual Hamiltonian paths in your graph. The unittest library does not support printing directly, so if you want to see the result of each test, you need to add some print statements or use a logging module.
