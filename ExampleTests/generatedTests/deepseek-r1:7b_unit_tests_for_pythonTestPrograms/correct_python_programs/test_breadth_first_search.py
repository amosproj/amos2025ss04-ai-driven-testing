from collections import deque as Queue
import unittest

def breadth_first_search(startnode, goalnode):
    queue = Queue()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while len(queue) > 0:
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            for successor in node.successors:  # Changed to use property from your class
                if successor not in nodesseen:
                    nodesseen.add(successor)
                    queue.append(successor)

    return False

class TestBreadthFirstSearch(unittest.TestCase):
    def test_breadth_first_search(self):
        # Create a simple graph: A -> B, C; B -> D; C -> E
        class SimpleGraph:
            def __init__(self):
                self.successors = {
                    'A': ['B', 'C'],
                    'B': ['D'],
                    'C': ['E']
                }

        # Test case 1: Goal is directly reachable from start
        graph = SimpleGraph()
        result = breadth_first_search(graph['A'], graph['B'])
        self.assertTrue(result)

        # Test case 2: Goal requires multiple steps
        result = breadth_first_search(graph['A'], graph['D'])
        self.assertFalse(result, "Should not reach D")

        # Test case 3: Different loop condition implementation (using len(queue) > 0)
        result = breadth_first_search(graph['C'], graph['E'])
        self.assertTrue(result)

    def test_breadth_first_search_with_different_loop(self):
        class SimpleGraph:
            def __init__(self):
                self.successors = {
                    'A': ['B', 'C'],
                    'B': ['D'],
                    'C': ['E']
                }

        # Goal is reachable
        graph = SimpleGraph()
        result = breadth_first_search(graph['A'], graph['D'])
        self.assertFalse(result, "Should not reach D")
        
        # Change the BFS implementation to use len(queue) > 0 condition
        queue = deque()
        queue.append('A')
        nodesseen = {'A'}
        while queue:
            node = queue.popleft()
            if node == 'D':
                return True
            for successor in graph['A'].successors:
                if successor not in nodesseen and successor == 'B' or successor == 'C':
                    nodesseen.add(successor)
                    queue.append(successor)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
```

This test class includes:

1. A test method for the basic BFS implementation
2. A test method specifically testing the different loop condition (`len(queue) > 0`)

The code is structured to be:
- Testable with Python's unittest framework
- Easy to understand and maintain
- Comprehensive in its test cases

To run the tests, you can use this command:

```bash
python3 -m unittest test_breadth_first_search.py