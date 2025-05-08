class Node:
    def __init__(
        self,
        value=None,
        successor=None,
        successors=[],
        predecessors=[],
        incoming_nodes=[],
        outgoing_nodes=[],
    ):
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


import unittest


class TestNodeMethods(unittest.TestCase):
    def setUp(self):
        self.node = Node(
            value=1,
            successor=2,
            successors=[3],
            predecessors=[4],
            incoming_nodes=[5],
            outgoing_nodes=[6],
        )

    def test_successor(self):
        self.assertEqual(self.node.successor(), 2)

    def test_successors(self):
        self.assertEqual(self.node.successors(), [3])

    def test_predecessors(self):
        self.assertEqual(self.node.predecessors(), [4])


if __name__ == "__main__":
    unittest.main()
