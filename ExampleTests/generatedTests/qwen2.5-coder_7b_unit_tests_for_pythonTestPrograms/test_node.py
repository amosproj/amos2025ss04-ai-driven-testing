import unittest


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

    def get_successor(self):
        return self.successor

    def get_successors(self):
        return self.successors

    def get_predecessors(self):
        return self.predecessors


class TestNode(unittest.TestCase):
    def test_init(self):
        node = Node(
            value=1,
            successor=2,
            successors=[3, 4],
            predecessors=[5, 6],
            incoming_nodes=[7, 8],
            outgoing_nodes=[9, 10],
        )
        self.assertEqual(node.value, 1)
        self.assertEqual(node.successor, 2)
        self.assertEqual(node.successors, [3, 4])
        self.assertEqual(node.predecessors, [5, 6])
        self.assertEqual(node.incoming_nodes, [7, 8])
        self.assertEqual(node.outgoing_nodes, [9, 10])

    def test_get_successor(self):
        node = Node(successor=2)
        self.assertEqual(node.get_successor(), 2)

    def test_get_successors(self):
        node = Node(successors=[3, 4])
        self.assertEqual(node.get_successors(), [3, 4])

    def test_get_predecessors(self):
        node = Node(predecessors=[5, 6])
        self.assertEqual(node.get_predecessors(), [5, 6])


if __name__ == "__main__":
    unittest.main()
