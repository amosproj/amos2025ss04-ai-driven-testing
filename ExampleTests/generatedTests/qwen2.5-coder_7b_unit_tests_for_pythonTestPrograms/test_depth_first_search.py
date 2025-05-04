import unittest

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

class TestDepthFirstSearch(unittest.TestCase):

    def test_depth_first_search_goal_found(self):
        # Create nodes
        a = Node('A')
        b = Node('B')
        c = Node('C')

        # Build graph: A -> B -> C
        a.add_successor(b)
        b.add_successor(c)

        # Search from A to C
        result = depth_first_search(a, c)
        
        self.assertTrue(result)

    def test_depth_first_search_goal_not_found(self):
        # Create nodes
        a = Node('A')
        b = Node('B')
        c = Node('C')

        # Build graph: A -> B -> C
        a.add_successor(b)
        b.add_successor(c)

        # Search from A to D (D does not exist)
        result = depth_first_search(a, 'D')
        
        self.assertFalse(result)

    def test_depth_first_search_single_node(self):
        # Create a single node
        a = Node('A')

        # Search for itself
        result = depth_first_search(a, a)
        
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()