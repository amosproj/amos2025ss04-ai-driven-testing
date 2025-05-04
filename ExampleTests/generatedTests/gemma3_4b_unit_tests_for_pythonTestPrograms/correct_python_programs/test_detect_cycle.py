class Node:
    def __init__(self, data):
        self.data = data
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


# Please generate a test class with unit tests for the above code using unittest. Return a python file containing the original code plus the test so that I just need to run the resulting file and i can see if the tests go through
class TestDetectCycle:
    def test_no_cycle(self):
        node1 = Node(1)
        node2 = Node(2)
        node1.successor = node2
        self.assertFalse(detect_cycle(node1))

    def test_cycle(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node1.successor = node2
        node2.successor = node3
        node3.successor = node1
        self.assertTrue(detect_cycle(node1))

    def test_single_node(self):
        node = Node(1)
        self.assertFalse(detect_cycle(node))

    def test_cycle_longer(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node4 = Node(4)
        node1.successor = node2
        node2.successor = node3
        node3.successor = node4
        node4.successor = node1
        self.assertTrue(detect_cycle(node1))

if __name__ == '__main__':
    unittest.main()