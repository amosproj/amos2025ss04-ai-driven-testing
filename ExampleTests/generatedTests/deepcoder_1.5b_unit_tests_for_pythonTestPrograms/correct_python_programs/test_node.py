class Node(unittest.TestCase):
    def __init__(self, value=None, successor=None, successors=None, predecessors=None, incoming_nodes=None, outgoing_nodes=None):
        self.value = value
        self.successor = successor if successor is not None else None
        self.successors = successors if successors is not None else []
        self.predecessors = predecessors if predecessors is not None else []
        self.incoming_nodes = incoming_nodes if incoming_nodes is not None else []
        self.outgoing_nodes = outgoing_nodes if outgoing_nodes is not None else []

    def successor(self):
        return self.successor

    def successors(self):
        return list(self.successors)

    def predecessors(self):
        return list(self.predecessors)

    def incoming_nodes(self):
        return list(self.incoming_nodes)

    def outgoing_nodes(self):
        return list(self.outgoing_nodes)

    def __repr__(self):
        return f"Node(value={self.value}, successor={self.successor!r}, successors={self.successors!r}, predecessors={self.predecessors!r}, incoming_nodes={self.incoming_nodes!r}, outgoing_nodes={self.outgoing_nodes!r})"

import unittest

from correct_python_programs.node import Node
from correct_python_programs.nodefromcorrect_python_programs import Node


class TestNode(unittest.TestCase):
    def test_node_value_none(self):
        node = Node()
        self assert node.value is None

    def test_node_value_set(self):
        node5 = Node(5)
        self assert node5.value == 5
        self assert node5.successor is not None

    def test_node_value_set_with_string(self):
        node_a = Node('a')
        self assert node_a.value == 'a'
        self assert node_a.successor is not None

    def test_set_all_attributes(self):
        node = Node(1, successor=2, successors=[3], predecessors=None, incoming_nodes=[], outgoing_nodes=[4])
        self assert node.value == 1
        self assert node.successor == 2
        self assert node.successors == [3]
        self assert node.predecessors is None
        self assert node.incoming_nodes is []
        self assert node.outgoing_nodes is [4]

    def test_successors(self):
        node = Node(5)
        self.assertEqual(node.successors, [])

    def test_predecessors(self):
        node = Node(6)
        self.assertEqual(node.predecessors, [])

    def test_incoming_nodes(self):
        node = Node(7, incoming_nodes=[8])
        self.assertEqual(incoming_nodes, [8])

    def test_outgoing_nodes(self):
        node = Node(9, outgoing_nodes=[10, 11])
        self.assertEqual(outgoing_nodes, [10, 11])

if __name__ == "__main__":
    unittest.main()