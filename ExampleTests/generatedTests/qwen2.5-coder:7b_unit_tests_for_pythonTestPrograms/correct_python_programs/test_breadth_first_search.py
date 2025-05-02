from collections import deque as Queue
import unittest

def breadth_first_search(startnode, goalnode):
    queue = Queue()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while len(queue) != 0:
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            queue.extend(node for node in node.successors if node not in nodesseen)
            nodesseen.update(node.successors)

    return False

class TestBreadthFirstSearch(unittest.TestCase):
    def test_breadth_first_search_success(self):
        # Create mock nodes
        class MockNode:
            def __init__(self, value, successors=None):
                self.value = value
                self.successors = set(successors) if successors else set()

        start_node = MockNode('A', {'B', 'C'})
        node_b = MockNode('B', {'D'})
        node_c = MockNode('C')
        node_d = MockNode('D')

        # Set up the goal node
        goal_node = node_d

        # Perform the search
        result = breadth_first_search(start_node, goal_node)

        # Check if the search was successful
        self.assertTrue(result)

    def test_breadth_first_search_failure(self):
        # Create mock nodes
        class MockNode:
            def __init__(self, value, successors=None):
                self.value = value
                self.successors = set(successors) if successors else set()

        start_node = MockNode('A', {'B', 'C'})
        node_b = MockNode('B', {'D'})
        node_c = MockNode('C')
        node_d = MockNode('D')

        # Set up a goal node that is not reachable
        goal_node = MockNode('E')

        # Perform the search
        result = breadth_first_search(start_node, goal_node)

        # Check if the search was unsuccessful
        self.assertFalse(result)

    def test_breadth_first_search_single_node(self):
        # Create mock nodes
        class MockNode:
            def __init__(self, value, successors=None):
                self.value = value
                self.successors = set(successors) if successors else set()

        start_node = MockNode('A')
        goal_node = start_node

        # Perform the search
        result = breadth_first_search(start_node, goal_node)

        # Check if the search was successful
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()