import unittest

class Node:
    def __init__(self, value=None, successor=None, successors=[], predecessors=[], incoming_nodes=[], outgoing_nodes=[]):
        self.value = value
        self.successor = successor
        self.successors = successors
        self.predecessors = predecessors
        self.incoming_nodes = incoming_nodes
        self.outgoing_nodes = outgoing_nodes

    def successor(self):
        return self.successor

    def successors(self):
        return self.successors

    def predecessors(self):
        return self.predecessors


class TestNode(unittest.TestCase):
    def test_init(self):
        node = Node(value=10)
        self.assertEqual(node.value, 10)
        self.assertIsNone(node.successor)
        self.assertListEqual(node.successors, [])
        self.assertListEqual(node.predecessors, [])
        self.assertListEqual(node.incoming_nodes, [])
        self.assertListEqual(node.outgoing_nodes, [])

    def test_successor(self):
        node = Node(value=10, successor=Node(value=20))
        self.assertEqual(node.successor.value, 20)
        self.assertIsNone(node.successor.successor)

    def test_successors(self):
        node = Node(value=10, successors=[Node(value=20), Node(value=30)])
        self.assertEqual(len(node.successors), 2)
        self.assertEqual(node.successors[0].value, 20)
        self.assertEqual(node.successors[1].value, 30)

    def test_predecessors(self):
        node = Node(value=10, predecessors=[Node(value=5)])
        self.assertEqual(len(node.predecessors), 1)
        self.assertEqual(node.predecessors[0].value, 5)

if __name__ == '__main__':
    unittest.main()