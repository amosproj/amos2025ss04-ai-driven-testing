class ListNode:
    def __init__(self, value=None):
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


import unittest
from typing import Optional

class TestDetectCycle(unittest.TestCase):
    def create_list_with_cycle(self, values: list) -> Optional[ListNode]:
        nodes = [ListNode(value) for value in values]
        for i in range(len(nodes) - 1):
            nodes[i].successor = nodes[i + 1]

        # Create cycle
        nodes[-1].successor = nodes[0]
        
        return nodes[0] if nodes else None

    def test_detect_cycle(self):
        node = self.create_list_with_cycle([1, 2, 3, 4])
        self.assertTrue(detect_cycle(node))

        node.successor.successor.successor.successor = node
        self.assertTrue(detect_cycle(node))

        node = self.create_list_with_cycle([])
        self.assertFalse(detect_cycle(node))

        node = self.create_list_with_cycle([1])
        self.assertFalse(detect_cycle(node))

if __name__ == '__main__':
    unittest.main()