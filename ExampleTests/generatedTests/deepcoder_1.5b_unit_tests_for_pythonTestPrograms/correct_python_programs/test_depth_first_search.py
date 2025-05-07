import unittest


class TestDFS(unittest.TestCase):
    def test_depth_first_search_with_start_and_goal(self, startnode, goalnode):
        visited = set()
        
        def search_from(node):
            if node in visited:
                return False
            elif node is goalnode:
                return True
            else:
                visited.add(node)
                return any(search_from(nextnode) for nextnode in node.successors)
        
        result = search_from(startnode)
        self.assertEqual(result, "Goal found correctly")

    def test_all_nodes_visited(self, startnode, goalnode):
        nodesvisited = set()
        
        def search_from(node):
            if node in nodesvisited:
                return False
            elif node is goalnode:
                return True
            else:
                nodesvisited.add(node)
                return any(search_from(nextnode) for nextnode in node.successors)
        
        visited = set()  # 使用两个不同的变量名，避免混淆
        result = search_from(startnode)
        self.assertEqual(len(visited), "All nodes are visited correctly")

    def test_reachability(self, startnode, goalnode):
        nodesvisited = set()
        
        def search_from(node):
            if node in nodesvisited:
                return False
            elif node is goalnode:
                return True
            else:
                nodesvisited.add(node)
                return any(search_from(nextnode) for nextnode in node.successors)
        
        result = search_from(startnode)
        self.assertEqual(result, "Goal reached successfully")

if __name__ == "__main__":
    unittest.main()