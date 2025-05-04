import unittest

class Node:
    def __init__(self, name):
        self.name = name
        self.incoming_nodes = []
        self.outgoing_nodes = []

    def add_incoming_node(self, node):
        self.incoming_nodes.append(node)

    def add_outgoing_node(self, node):
        self.outgoing_nodes.append(node)

class TopologicalOrderingTest(unittest.TestCase):

    def test_topological_ordering_with_cycle(self):
        # Create nodes
        a = Node('A')
        b = Node('B')
        c = Node('C')
        d = Node('D')

        # Add edges
        a.add_outgoing_node(b)
        a.add_outgoing_node(c)
        b.add_outgoing_node(d)

        # Run the topological ordering function
        result = topological_ordering([a, b, c, d])

        # Check if the result is as expected (should be [A, B, C, D])
        self.assertEqual(result, [a, b, c, d], "Test failed for cycle")

    def test_topological_ordering_without_cycle(self):
        # Create nodes
        a = Node('A')
        b = Node('B')
        c = Node('C')

        # Add edges
        a.add_outgoing_node(b)
        c.add_outgoing_node(a)

        # Run the topological ordering function
        result = topological_ordering([a, b, c])

        # Check if the result is as expected (should be [A, B, C])
        self.assertEqual(result, [a, b, c], "Test failed for no cycle")

    def test_topological_ordering_with_single_node(self):
        # Create a single node
        a = Node('A')

        # Run the topological ordering function
        result = topological_ordering([a])

        # Check if the result is as expected (should be [A])
        self.assertEqual(result, [a], "Test failed for single node")

if __name__ == '__main__':
    unittest.main()