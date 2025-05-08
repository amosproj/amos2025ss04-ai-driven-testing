import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.successor = None


def reverse_linked_list(node):
    prevnode = None
    while node:
        nextnode = node.successor
        node.successor = prevnode
        prevnode = node
        node = nextnode
    return prevnode


class TestReverseLinkedList(unittest.TestCase):
    def test_reverse_linked_list_empty(self):
        result = reverse_linked_list(None)
        self.assertIsNone(result)

    def test_reverse_linked_list_single_node(self):
        node1 = Node(1)
        result = reverse_linked_list(node1)
        self.assertEqual(result.value, 1)
        self.assertIsNone(result.successor)

    def test_reverse_linked_list_two_nodes(self):
        node1 = Node(1)
        node2 = Node(2)
        node1.successor = node2
        result = reverse_linked_list(node1)
        self.assertEqual(result.value, 2)
        self.assertIsNotNone(result.successor)
        self.assertEqual(result.successor.value, 1)
        self.assertIsNone(result.successor.successor)

    def test_reverse_linked_list_three_nodes(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node1.successor = node2
        node2.successor = node3
        result = reverse_linked_list(node1)
        self.assertEqual(result.value, 3)
        self.assertIsNotNone(result.successor)
        self.assertEqual(result.successor.value, 2)
        self.assertIsNotNone(result.successor.successor)
        self.assertEqual(result.successor.successor.value, 1)
        self.assertIsNone(result.successor.successor.successor)


if __name__ == "__main__":
    unittest.main()
