from collections import deque as Queue
import unittest

class TestBreadthFirstSearch(unittest.TestCase):
    def setUp(self):
        # Define a simple node class for testing
        self.Node = type('Node', (object,), {
            'successors': property(lambda self: ['A', 'B']),
            '__init__': lambda self, value: setattr(self, '_value', value)
        })

        self.startnode = self.Node('Start')
        self.goalnode = self.Node('Goal')

    def test_breadth_first_search_success(self):
        # Test the function with a simple graph
        self.assertTrue(breadth_first_search(self.startnode, self.goalnode))

    def test_breadth_first_search_failure(self):
        # Test the function with a graph where the goal is not reachable
        unvisited_node = self.Node('Unvisited')
        self.assertFalse(breadth_first_search(self.startnode, unvisited_node))

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)