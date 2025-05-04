def topological_ordering(nodes):
    ordered_nodes = [node for node in nodes if not node.incoming_nodes]

    for node in ordered_nodes:
        for nextnode in node.outgoing_nodes:
            if set(ordered_nodes).issuperset(nextnode.incoming_nodes) and nextnode not in ordered_nodes:
                ordered_nodes.append(nextnode)

    return ordered_nodes


class Node:
    def __init__(self, name):
        self.name = name
        self.incoming_nodes = []
        self.outgoing_nodes = []

    def add_incoming(self, node):
        self.incoming_nodes.append(node)

    def add_outgoing(self, node):
        self.outgoing_nodes.append(node)


import unittest


class TestTopologicalOrdering(unittest.TestCase):
    def test_empty_input(self):
        nodes = []
        result = topological_ordering(nodes)
        self.assertEqual(result, [])

    def test_single_node(self):
        node1 = Node("A")
        result = topological_ordering([node1])
        self.assertEqual(result, [node1])

    def test_simple_graph(self):
        node1 = Node("A")
        node2 = Node("B")
        node3 = Node("C")

        node1.add_outgoing(node2)
        node1.add_outgoing(node3)

        result = topological_ordering([node1, node2, node3])
        self.assertEqual(result, [node1, node2, node3])

    def test_graph_with_cycle(self):
        node1 = Node("A")
        node2 = Node("B")
        node3 = Node("C")

        node1.add_outgoing(node2)
        node2.add_incoming(node1)

        with self.assertRaises(AssertionError):
            topological_ordering([node1, node2, node3])


if __name__ == "__main__":
    unittest.main()