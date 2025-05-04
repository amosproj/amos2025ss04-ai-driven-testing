import unittest

class Node:
    def __init__(self, value):
        self.value = value
        self.successor = None

def detect_cycle(node):
    hare = tortoise = node

    while True:
        if hare is None or hare.successor is None:
            return False

        tortoise = tortoise.successor
        hare = hare.successor.successor

        if hare is tortoise:
            return True

class TestDetectCycle(unittest.TestCase):

    def test_no_cycle(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)

        node1.successor = node2
        node2.successor = node3

        self.assertFalse(detect_cycle(node1))

    def test_cycle_at_head(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)

        node1.successor = node2
        node2.successor = node3
        node3.successor = node1

        self.assertTrue(detect_cycle(node1))

    def test_cycle_in_middle(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node4 = Node(4)

        node1.successor = node2
        node2.successor = node3
        node3.successor = node4
        node4.successor = node2

        self.assertTrue(detect_cycle(node1))

    def test_empty_list(self):
        self.assertFalse(detect_cycle(None))

if __name__ == '__main__':
    unittest.main()