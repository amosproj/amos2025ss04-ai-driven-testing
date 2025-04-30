import unittest

def shortest_paths(source, weight_by_edge):
    weight_by_node = {
        v: float('inf') for u, v in weight_by_edge
    }
    weight_by_node[source] = 0

    for i in range(len(weight_by_node) - 1):
        for (u, v), weight in weight_by_edge.items():
            weight_by_node[v] = min(
                weight_by_node[u] + weight,
                weight_by_node[v]
            )

    return weight_by_node


class TestShortestPaths(unittest.TestCase):

    def test_empty_graph(self):
        weight_by_edge = {}
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result, {'A': 0})

    def test_simple_graph(self):
        weight_by_edge = {
            ('A', 'B'): 5,
            ('B', 'C'): 3,
        }
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result, {'A': 0, 'B': 5, 'C': 8})

    def test_graph_with_multiple_paths(self):
        weight_by_edge = {
            ('A', 'B'): 1,
            ('A', 'C'): 4,
            ('B', 'C'): 2,
            ('C', 'D'): 1,
        }
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result, {'A': 0, 'B': 1, 'C': 2, 'D': 3})

    def test_disconnected_graph(self):
        weight_by_edge = {
            ('A', 'B'): 1,
            ('C', 'D'): 2
        }
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result, {'A': 0, 'B': 1, 'C': 2, 'D': float('inf')})
    
    def test_self_loop(self):
        weight_by_edge = {
            ('A', 'A'): 5
        }
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result, {'A': 0})
        
if __name__ == '__main__':
    unittest.main()