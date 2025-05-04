from typing import *
from collections import *

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


"""
def detect_cycle(node):
    hare = tortoise = node

    while True:
        if hare.successor is None or hare.successor.successor is None:
            return False

        tortoise = tortoise.successor
        hare = hare.successor.successor

        if hare is tortoise:
            return True
"""


class TestDetectCycle(unittest.TestCase):
    def test_detect_cycle(self):
        # Create a linked list with a cycle
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)

        node1.successor = node2
        node2.successor = node3
        node3.successor = node2  # Creating a cycle

        self.assertTrue(detect_cycle(node1))

    def test_detect_no_cycle(self):
        # Create a linked list without a cycle
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)

        node1.successor = node2
        node2.successor = node3

        self.assertFalse(detect_cycle(node1))

    def test_empty_list(self):
        # Test with an empty list
        self.assertFalse(detect_cycle(None))

    def test_single_node_no_cycle(self):
        # Test with a single node without a cycle
        node1 = Node(1)
        self.assertFalse(detect_cycle(node1))

if __name__ == '__main__':
    unittest.main()