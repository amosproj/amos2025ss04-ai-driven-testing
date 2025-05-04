class Node:
    def __init__(self, data):
        self.data = data
        self.successors = []

    def add_successor(self, successor):
        self.successors.append(successor)

    def __repr__(self):
        return f"Node({self.data})"


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


import unittest

class TestDepthFirstSearch(unittest.TestCase):

    def setUp(self):
        self.node_a = Node("A")
        self.node_b = Node("B")
        self.node_c = Node("C")
        self.node_d = Node("D")
        self.node_e = Node("E")

        self.node_a.add_successor(self.node_b)
        self.node_a.add_successor(self.node_c)
        self.node_b.add_successor(self.node_d)
        self.node_c.add_successor(self.node_e)

    def test_dfs_find_goal(self):
        self.assertTrue(depth_first_search(self.node_a, self.node_e))

    def test_dfs_no_goal(self):
        self.assertFalse(depth_first_search(self.node_a, self.node_b))

    def test_dfs_start_goal(self):
        self.assertTrue(depth_first_search(self.node_a, self.node_a))

    def test_dfs_empty_successors(self):
        self.node_f = Node("F")
        self.node_a.add_successor(self.node_f)
        self.node_f.add_successor(self.node_f)
        self.node_a.add_successor(self.node_f)

        self.assertTrue(depth_first_search(self.node_a, self.node_f))

    def test_dfs_complex_graph(self):
        node1 = Node("1")
        node2 = Node("2")
        node3 = Node("3")
        node4 = Node("4")
        node5 = Node("5")
        node6 = Node("6")

        node1.add_successor(node2)
        node1.add_successor(node3)
        node2.add_successor(node4)
        node3.add_successor(node4)
        node4.add_successor(node5)
        node5.add_successor(node6)

        self.assertTrue(depth_first_search(node1, node6))
        self.assertFalse(depth_first_search(node1, node7))  # Non-existent node

if __name__ == '__main__':
    unittest.main()