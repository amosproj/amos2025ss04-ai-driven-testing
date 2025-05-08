import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.incoming_nodes = []
        self.outgoing_nodes = []


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


class TestTopologicalOrdering(unittest.TestCase):
    def test_topological_ordering(self):
        # Create nodes
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node4 = Node(4)

        # Create directed edges
        node1.outgoing_nodes.append(node2)
        node1.outgoing_nodes.append(node3)
        node2.outgoing_nodes.append(node4)
        node3.outgoing_nodes.append(node4)

        # Add nodes to the list
        nodes = [node1, node2, node3, node4]

        # Expected result
        expected_result = [node1, node2, node3, node4]

        # Run the function
        result = topological_ordering(nodes)

        # Check if the result matches the expected output
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
