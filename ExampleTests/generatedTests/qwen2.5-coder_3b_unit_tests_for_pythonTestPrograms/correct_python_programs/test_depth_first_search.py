import unittest

class TestDepthFirstSearch(unittest.TestCase):
    def setUp(self):
        # Define a simple graph for testing purposes
        class Node:
            def __init__(self, value):
                self.value = value
                self.successors = []

            def add_successor(self, successor):
                self.successors.append(successor)

        # Create some nodes and establish relationships between them
        node_a = Node('A')
        node_b = Node('B')
        node_c = Node('C')
        node_d = Node('D')

        node_a.add_successor(node_b)
        node_a.add_successor(node_c)
        node_b.add_successor(node_d)

        # Set up the start and goal nodes
        self.start_node = node_a
        self.goal_node = node_d

    def test_depth_first_search(self):
        result = depth_first_search(self.start_node, self.goal_node)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()