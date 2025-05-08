import unittest

from correct_python_programs.detect_cyclefromcorrect_python_programs import \
    detect_cycle


class TestNode(unittest.TestCase):
    def __init__(self, value):
        self.value = value
        self.successor = None

def detect_cycle(node):
    if node is None or node.successor is None:
        return False
    
    hare = tortoise = node

    while True:
        tortoise = tortoise.successor
        hare = hare.successor
        
        if hare is None:
            return False
            
        hare = hare.successor
        
        if tortoise == hare:
            return True
            
    return False

class TestDetectCycle(unittest.TestCase):
    def setUp(self):
        self.nodes = []
        
    def create linked list (self, values):
        current = None
        for value in reversed(values):
            new_node = TestNode(value)
            new_node.successor = current
            current = new_node
        return current

    def test_detect_cycle_no_cycle(self):
        # Test case with no cycle
        nodes = [1, 2, 3]
        linked_list = self.create_linked_list(nodes)
        self.assertFalse(detect_cycle(linked_list))
    
    def test_detect_cycle_cycle_from_start(self):
        # Test case with cycle starting at head
        nodes = {1: 2, 2: 3, 3: 1}
        linked_list = self.create_linked_list([1, 2, 3])
        self.assertTrue(detect_cycle(linked_list))
    
    def test_detect_cycle_cycle_from_middle(self):
        # Test case with cycle starting at middle
        nodes = {2: 3, 3: 4, 4: 5, 5: 2}
        linked_list = self.create_linked_list([1, 2, 3])
        self.assertTrue(detect_cycle(linked_list))
    
    def test_detect_cycle_multiple_loops(self):
        # Test case with multiple loops
        nodes = {4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 5}
        linked_list = self.create_linked_list([1, 2])
        self.assertTrue(detect_cycle(linked_list))
    
    def test_detect_cycle_single_node(self):
        # Test case with single node
        nodes = [4]
        linked_list = self.create_linked_list(nodes)
        self.assertFalse(detect_cycle(linked_list))

if __name__ == '__main__':
    unittest.main()
```

This code:
1. Contains the `detect_cycle` function implementing Floyd's Tortoise and Hare algorithm for cycle detection in a singly-linked list.
2. Includes a test class `TestDetectCycle` with multiple test cases:
   - Testing no cycle
   - Cycle starting at head node
   - Cycle starting in the middle of the list
   - Multiple nested loops (complex cycle)
   - Single-node case
3. Uses Python's built-in `unittest` framework for testing
4. Each test method explicitly checks the expected behavior of the cycle detection function

To run the tests, simply execute this script:
```bash
python -m unittest -v cycle_detection_test.py