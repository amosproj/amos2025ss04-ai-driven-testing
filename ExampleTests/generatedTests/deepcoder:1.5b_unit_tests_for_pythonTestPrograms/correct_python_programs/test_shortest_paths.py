import unittest
from graph import shortest_paths  # Assuming the function is in a module named graph

class TestShortestPaths(unittest.TestCase):
    def test_shortest_path_from_source(self, source):
        # Create a simple graph
        graph = {
            'A': {'B': 1},
            'B': {'C': 1}
        }
        
        # Calculate shortest paths from 'A'
        distances = shortest_paths(graph, weight_by_edge=None)
        
        # Check if distance to 'C' is correct
        self.assertEqual(distances['C'], 2)

if __name__ == '__main__':
    unittest.main()