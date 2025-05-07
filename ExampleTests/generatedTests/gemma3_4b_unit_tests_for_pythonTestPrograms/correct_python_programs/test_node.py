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

    def successor(self):
        return self.successor

    def successors(self):
        return self.successors

    def predecessors(self):
        return self.predecessors


class TestNode(unittest.TestCase):
    def test_successor(self):
        node = Node("A")
        self.assertEqual(node.successor(), "A")

        node = Node("B", successor="C")
        self.assertEqual(node.successor(), "C")

    def test_successors(self):
        node = Node("A", successors=["B", "C"])
        self.assertEqual(node.successors(), ["B", "C"])

        node = Node("D", successors=[])
        self.assertEqual(node.successors(), [])

    def test_predecessors(self):
        node = Node("A", predecessors=["B"])
        self.assertEqual(node.predecessors(), ["B"])

        node = Node("E", predecessors=[])
        self.assertEqual(node.predecessors(), [])

    def test_init(self):
        node = Node()
        self.assertIsNone(node.value)
        self.assertIsNone(node.successor)
        self.assertEqual(len(node.successors), 0)
        self.assertEqual(len(node.predecessors), 0)
        self.assertEqual(len(node.incoming_nodes), 0)
        self.assertEqual(len(node.outgoing_nodes), 0)

    def test_empty_lists(self):
        node = Node()
        self.assertEqual(len(node.successors), 0)
        self.assertEqual(len(node.predecessors), 0)
        self.assertEqual(len(node.incoming_nodes), 0)
        self.assertEqual(len(node.outgoing_nodes), 0)


if __name__ == "__main__":
    unittest.main()
