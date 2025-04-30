import unittest
from collections import deque as Queue

def breadth_first_search(startnode, goalnode):
    queue = Queue()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while queue:
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            queue.extend(node for node in node.successors if node not in nodesseen)
            nodesseen.update(node.successors)

    return False


class TestBreadthFirstSearch(unittest.TestCase):

    def test_bfs_simple(self):
        class Node:
            def __init__(self, data):
                self.data = data
                self.successors = []

            def __eq__(self, other):
                return self.data == other.data

        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node1.successors = [node2, node3]
        node2.successors = []
        node3.successors = []
        goal = node3

        self.assertTrue(breadth_first_search(node1, goal))

    def test_bfs_no_path(self):
        class Node:
            def __init__(self, data):
                self.data = data
                self.successors = []

            def __eq__(self, other):
                return self.data == other.data

        node1 = Node(1)
        node2 = Node(2)
        node1.successors = [node2]
        node2.successors = []
        goal = Node(4)

        self.assertFalse(breadth_first_search(node1, goal))

    def test_bfs_start_equals_goal(self):
        class Node:
            def __init__(self, data):
                self.data = data
                self.successors = []

            def __eq__(self, other):
                return self.data == other.data

        node1 = Node(1)
        self.assertTrue(breadth_first_search(node1, node1))

    def test_bfs_empty_successors(self):
        class Node:
            def __init__(self, data):
                self.data = data
                self.successors = []

            def __eq__(self, other):
                return self.data == other.data

        node1 = Node(1)
        node1.successors = []
        goal = node1

        self.assertTrue(breadth_first_search(node1, goal))

if __name__ == '__main__':
    unittest.main()