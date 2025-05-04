def reverse_linked_list(node):
    prevnode = None
    while node:
        nextnode = node.successor
        node.successor = prevnode
        prevnode, node = node, nextnode
    return prevnode


import unittest

class ListNode:
    def __init__(self, value=0, successor=None):
        self.value = value
        self.successor = successor

    def __repr__(self):
        return f"ListNode({self.value})"

class TestReverseLinkedList(unittest.TestCase):

    def test_reverse_linked_list(self):
        node1 = ListNode(1)
        node2 = ListNode(2)
        node3 = ListNode(3)

        node1.successor = node2
        node2.successor = node3

        reversed_head = reverse_linked_list(node1)

        self.assertEqual(reversed_head.value, 3)
        self.assertEqual(reversed_head.successor.value, 2)
        self.assertEqual(reversed_head.successor.successor.value, 1)


if __name__ == '__main__':
    unittest.main()