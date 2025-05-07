class Node:
    def __init__(self, name):
        self.name = name
        self.incoming_nodes = []
        self.outgoing_nodes = []

    def __repr__(self):
        return f"Node({self.name})"


def topological_ordering(nodes):
    ordered_nodes = [node for node in nodes if not node.incoming_nodes]

    for node in ordered_nodes:
        for nextnode in node.outgoing_nodes:
            if (
                set(ordered_nodes).issuperset(nextnode.incoming_nodes)
                and nextnode not in ordered_nodes
            ):
                ordered_nodes.append(nextnode)

    return ordered_nodes


import unittest


class TestTopologicalOrdering(unittest.TestCase):
    def test_empty_graph(self):
        nodes = [Node("A"), Node("B"), Node("C")]
        expected_order = []
        self.assertEqual(topological_ordering(nodes), expected_order)

    def test_simple_chain(self):
        nodes = [Node("A"), Node("B"), Node("C")]
        nodes[0].outgoing_nodes.append(nodes[1])
        nodes[1].outgoing_nodes.append(nodes[2])
        ordered_nodes = topological_ordering(nodes)
        self.assertEqual(ordered_nodes, [Node("A"), Node("B"), Node("C")])

    def test_branching_graph(self):
        nodes = [Node("A"), Node("B"), Node("C"), Node("D")]
        nodes[0].outgoing_nodes.append(nodes[1])
        nodes[1].outgoing_nodes.append(nodes[2])
        nodes[2].outgoing_nodes.append(nodes[3])
        ordered_nodes = topological_ordering(nodes)
        self.assertEqual(
            ordered_nodes, [Node("A"), Node("B"), Node("C"), Node("D")]
        )

    def test_complex_graph(self):
        nodes = [Node("A"), Node("B"), Node("C"), Node("D"), Node("E")]
        nodes[0].outgoing_nodes.append(nodes[1])
        nodes[1].outgoing_nodes.append(nodes[2])
        nodes[2].outgoing_nodes.append(nodes[3])
        nodes[3].outgoing_nodes.append(nodes[4])
        ordered_nodes = topological_ordering(nodes)
        self.assertEqual(
            ordered_nodes,
            [Node("A"), Node("B"), Node("C"), Node("D"), Node("E")],
        )

    def test_cyclic_graph(self):
        nodes = [Node("A"), Node("B")]
        nodes[0].outgoing_nodes.append(nodes[1])
        nodes[1].outgoing_nodes.append(nodes[0])
        ordered_nodes = topological_ordering(nodes)
        self.assertEqual(ordered_nodes, [Node("A"), Node("B")])


if __name__ == "__main__":
    unittest.main()
