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
    def test_constructor_value_successor_predecessors(self):
        node = Node(
            value=1,
            successor="next",
            successors=["a", "b"],
            predecessors=["pre"],
            incoming_nodes=[],
            outgoing_nodes=[],
        )

        self.assertEqual(node.value, 1)
        self.assertIsInstance(node.successor, str) and node.successor == "next"
        self.assertListEqual(node.successors, ["a", "b"])
        self.assertListEqual(node.predecessors, ["pre"])

    def test_successor(self):
        dummy_node = Node(value=10)

        successor_value = 20
        dummy_node.successor = successor_value

        succ = dummy_node.successor()

        # Testing the direct return of a value assigned to 'successor'
        self.assertEqual(succ, successor_value)

    def test_successors(self):
        node = Node(successors=["node1", "node2"])

        successors_list = node.successors()

        self.assertListEqual(successors_list, ["node1", "node2"])

    def test_predecessors(self):
        dummy_node = Node(predecessors=["prev1", "prev2"], predecessors=[])

        pred_values = dummy_node.predecessors()

        # Testing the direct return of a list assigned to 'predecessors'
        self.assertListEqual(pred_values, ["prev1", "prev2"])


if __name__ == "__main__":
    unittest.main()
