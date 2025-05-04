import unittest

class Node:
    def __init__(self, data):
        self.data = data
        self.successor = None

def reverse_linked_list(node):
    prevnode = None
    while node:
        nextnode = node.successor
        node.successor = prevnode
        prevnode, node = node, nextnode
    return prevnode

class TestReverseLinkedList(unittest.TestCase):

    def test_empty_list(self):
        self.assertIsNone(reverse_linked_list(None))

    def test_single_node(self):
        head = Node(1)
        new_head = reverse_linked_list(head)
        self.assertEqual(new_head.data, 1)
        self.assertIsNone(new_head.successor)

    def test_multiple_nodes(self):
        head = Node(1)
        head.successor = Node(2)
        head.successor.successor = Node(3)
        new_head = reverse_linked_list(head)

        self.assertEqual(new_head.data, 3)
        self.assertEqual(new_head.successor.data, 2)
        self.assertEqual(new_head.successor.data, 1)
        self.assertIsNone(new_head.successor)

    def test_already_reversed(self):
        head = Node(1)
        head.successor = Node(2)
        head.successor.successor = Node(3)
        new_head = reverse_linked_list(head)
        self.assertEqual(new_head.data, 3)
        self.assertEqual(new_head.successor.data, 2)
        self.assertEqual(new_head.successor.data, 1)
        self.assertIsNone(new_head.successor)


if __name__ == '__main__':
    unittest.main()