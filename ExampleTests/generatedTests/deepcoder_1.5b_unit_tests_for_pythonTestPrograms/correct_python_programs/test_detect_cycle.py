import unittest


class Testdetect_cycle:
    def setup(self, instance):
        self.node = instance()

    def test_detect_cycle_no_cycle(self, node):
        result = self.detect_cycle(node)
        assert not result, "No cycle should return False"

    def test_detect_cycle_single_node(self, node):
        result = self.detect_cycle(node)
        assert result, "Single node should be considered a cycle"

    def test_detect_cycle_multiple_nodes(self, node):
        # Create two separate cycles
        c1 = Node(1)
        c2 = Node(2)
        c3 = Node(3)

        def create_cycle(node):
            self._create_node(c1)
            self._create_node(c2)
            self._create_node(c3)

        def _create_node(node):
            node.successor = node
            yield node
            next_node = Node()
            if not next_node:
                result = self.test_detect_cycle(next_node)
                assert False, "Test should fail for empty nodes"
                return next_node
            next_node.successor = next_node
            yield next_node

        create_cycle(c1)
        create_cycle(c2)
        create_cycle(c3)

        node = c1
        result = self.detect_cycle(node)
        assert result, "Multiple nodes in cycles should detect a cycle"

    def test_detect_cycle_large_cycle(self, node):
        # Create one large cycle with multiple nodes
        c1 = Node(1)
        c2 = Node(2)
        c3 = Node(3)

        def create_large_cycle(node):
            node.successor = next_node
            yield node
            next_node = Node()
            if not next_node:
                result = self.test_detect_cycle(next_node)
                assert False, "Test should fail for empty nodes"
                return next_node
            next_node.successor = next_node
            yield next_node

        create_large_cycle(c1)
        c2.successor = c3
        c3.successor = c2
        node = c1
        result = self.detect_cycle(node)
        assert result, "Large cycle should detect a cycle"

    def main(self):
        test_cases = [
            (None, "No cycle in acyclic graph"),
            (True, "Single node is considered a cycle"),
            (False, "Two separate cycles exist"),
            (True, "Large cycle with multiple nodes exists"),
        ]

        for no_cycle, name in zip(
            [None, True, False, True],
            [
                "No cycle in acyclic graph",
                "Single node is considered a cycle",
                "Two separate cycles exist",
                "Large cycle with multiple nodes exists",
            ],
        ):
            self.setup(lambda: Node(no_cycle))
            result = self.detect_cycle(node)
            assert not no_cycle and (
                result if no_cycle is None else result
            ), f"{name} should be {result}"

        unittest.main()
