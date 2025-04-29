from collections import deque

def breadth_first_search(startnode, goalnode):
    queue = deque([startnode])

    nodesseen = set()
    nodesseen.add(startnode)

    while len(queue) > 0:
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            for successor in node.successors():
                if successor not in nodesseen:
                    queue.append(successor)
                    nodesseen.add(successor)

    return False

import unittest


class TestBreadthFirstSearch(unittest.TestCase):

    def test_success(self):
        class MockNode(object):
            def __init__(self, successors=None):
                self._successors = successors if successors is not None else []
            
            def successors(self):
                return iter(self._successors)

        # Construct a simple graph
        node_a = MockNode()
        node_b = MockNode([node_c])
        node_c = MockNode(successors=[node_d, node_e])
        node_d = MockNode()
        node_e = MockNode()

        node_a.successors = [node_b]
        node_b.successors.append(node_c)
        node_c.successors.extend([node_d, node_e])

        # Test successful search
        self.assertTrue(breadth_first_search(node_a, node_d))

    def test_failure(self):
        class MockNode(object):
            def __init__(self, successors=None):
                self._successors = successors if successors is not None else []

            def successors(self):
                return iter(self._successors)

        # Construct a graph where goalnode cannot be reached
        node_a = MockNode()
        node_b = MockNode([node_c])
        node_c = MockNode(successors=[node_d])

        node_a.successors = [node_b]
        node_b.successors.append(node_c)
        
        self.assertFalse(breadth_first_search(node_a, node_e))

    def test_no_successors(self):
        class Node(object):
            pass

        no_node = Node()

        # Test when the startnode has no successors
        with unittest.TestCase().assertRaises(RuntimeError):  # Expect RuntimeError since we cannot get next elements from empty iterables.
            breadth_first_search(no_node, node_b)  # Assuming `node_b` was defined somewhere above.


if __name__ == '__main__':
    unittest.main()