import unittest


class Node:
    def __init__(self, name):
        self.name = name
        self.incoming_nodes = set()
        self.outgoing_nodes = []


def topological_ordering(nodes):
    ordered_nodes = [node for node in nodes if not node.incoming_nodes]

    while True:
        moved_in_this_cycle = False

        for node in list(
            ordered_nodes
        ):  # Make a copy of the list since we're modifying it
            for nextnode in node.outgoing_nodes:
                if set([n.name for n in ordered_nodes]).issuperset(
                    nextnode.incoming_nodes
                ) and not any(n == nextnode for n in ordered_nodes):
                    moved_in_this_cycle = True
                    break

        # If no nodes were moved, we are done.
        if not moved_in_this_cycle:
            return [
                node for node in sorted(ordered_nodes, key=lambda x: x.name)
            ]


def create_example_graph():
    a = Node("A")
    b = Node("B")
    c = Node("C")

    # A -> B
    a.outgoing_nodes.append(b)

    # A -> C
    a.outgoing_nodes.append(c)

    return [a, b, c]


class TestTopologicalOrdering(unittest.TestCase):
    def test_ordering_empty_list(self):
        self.assertEqual(topological_ordering([]), [])

    def test_ordering_single_node(self):
        node = Node("A")
        nodes = [node]
        result = topological_ordering(nodes)
        for n in sorted(
            result, key=lambda x: x.name
        ):  # Sort to match expected order
            self.assertTrue(n == node)

    def test_ordering_two_nodes_with_dependency_a_on_b(self):
        a = Node("A")
        b = Node("B")

        nodes = [a]
        topological_order(a.outgoing_nodes, [])
        result = topological_ordering(nodes)

        for n in sorted(
            result, key=lambda x: x.name
        ):  # Sort to match expected order
            self.assertTrue(n == a)

    def test_ordering_two_nodes_with_dependency_a_on_b(self):
        nodes = create_example_graph()
        ordered_result = topological_ordering(sorted(nodes))
        result_names = [
            n.name for n in sorted(ordered_result, key=lambda x: x.name)
        ]

        expected_order = ["A", "B", "C"]
        self.assertEqual(result_names, expected_order)

    def test_topological_sort_cycle(self):
        # Create a cycle A -> B and B <-> C
        nodes = create_example_graph()
        for node in sorted(
            nodes
        ):  # Sort to make sure we check with consistent starting order.
            if "B" not in [n.name for n in ordered_nodes]:
                raise Exception(
                    "Cycle detected. Topological sorting is impossible."
                )


if __name__ == "__main__":
    unittest.main()
