Sure, here are some unit tests for the Graph class using python unittest library. 

```python
import unittest
from typing import List
from graph import Graph

class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4), (1, 3)]
        self.graph = Graph(self.edges)
        
    def test_make_graph(self):
        graph = self.graph.graph
        for edge in self.edges:
            u, v = edge
            self.assertIn(v, graph[u])
            self.assertIn(u, graph[v])
            
    def test_visit(self):
        node = 5
        self.graph.visit(node)
        self.assertTrue(self.graph.visited[node])
        
    def test_un_visit(self):
        node = 1
        self.graph.visit(node)
        self.graph.un_visit(node)
        self.assertFalse(self.graph.visited[node])
        
    def test_all_nodes_are_visited(self):
        nodes = [i for i in range(1, 5)]
        for node in nodes:
            self.graph.visit(node)
        self.assertTrue(self.graph.all_nodes_are_visited())
        
    def test_get_hamiltonian_path(self):
        start = 1
        expected = [[2, 4, 3, 1], [2, 1]]
        result: List[List[int]] = self.graph.get_hamiltonian_path(start)
        
        for path in result:
            self.assertIn(list(reversed(path)), expected)
            
if __name__ == "__main__":
    unittest.main()
```
The tests are creating a Graph instance and checking if the methods work as intended, including whether they correctly mark nodes as visited or not (`test_visit`, `test_un_visit`), check if all nodes have been visited (`test_all_nodes_are_visited`) and find correct Hamiltonian paths(`test_get_hamiltonian_path`).
