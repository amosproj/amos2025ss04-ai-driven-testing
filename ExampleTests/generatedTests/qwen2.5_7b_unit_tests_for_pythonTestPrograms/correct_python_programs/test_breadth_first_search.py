from collections import deque as Queue


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
            queue.extend(
                node for node in node.successors if node not in nodesseen
            )
            nodesseen.update(node.successors)

    return False


from collections import deque as Queue
import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.successors = []

    def add_successor(self, node):
        self.successors.append(node)


class TestBreadthFirstSearch(unittest.TestCase):
    def setUp(self):
        self.node_a = Node("A")
        self.node_b = Node("B")
        self.node_c = Node("C")
        self.node_d = Node("D")

        self.node_a.add_successor(self.node_b)
        self.node_a.add_successor(self.node_c)
        self.node_b.add_successor(self.node_d)

    def test_breadth_first_search_positive_case(self):
        result = breadth_first_search(self.node_a, self.node_d)
        self.assertTrue(result)

    def test_breadth_first_search_negative_case(self):
        result = breadth_first_search(self.node_a, self.node_c)
        self.assertFalse(result)

    def test_breadth_first_search_startnode_is_goalnode(self):
        result = breadth_first_search(self.node_b, self.node_b)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
