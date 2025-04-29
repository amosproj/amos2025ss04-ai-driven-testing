def depth_first_search(startnode, goalnode):
    nodesvisited = set()

    def search_from(node):
        if node in nodesvisited:
            return False
        elif node is goalnode:
            return True
        else:
            nodesvisited.add(node)
            return any(
                search_from(nextnode) for nextnode in node.successors
            )

    return search_from(startnode)


class Node:
    def __init__(self, value):
        self.value = value
        self.successors = []

    def add_successor(self, successor):
        self.successors.append(successor)

# Test class to test the depth_first_search function
import unittest

class TestDepthFirstSearch(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(1)
        self.node2 = Node(2)
        self.node3 = Node(3)
        self.node4 = Node(4)
        self.node5 = Node(5)

    def test_depth_first_search(self):
        # Create a graph
        self.node1.add_successor(self.node2)
        self.node1.add_successor(self.node3)
        self.node2.add_successor(self.node4)
        self.node3.add_successor(self.node5)

        # Test for goal node in the graph
        result = depth_first_search(self.node1, self.node4)
        self.assertTrue(result)

        # Test for a node not in the graph
        result = depth_first_search(self.node1, self.node5)
        self.assertFalse(result)

    def test_depth_first_search_with_cycle(self):
        # Create a cycle
        self.node1.add_successor(self.node2)
        self.node2.add_successor(self.node3)
        self.node3.add_successor(self.node1)  # Cycle

        # Test for goal node in the graph (should not get stuck in infinite loop)
        result = depth_first_search(self.node1, self.node2)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()