import unittest
from depth_first_search import depth_first_search

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
```

不要使用以下代码，因为它们会生成与问题无关的输出：

```python
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

# Please generate a test class with unit tests for the above code using unittest. Return a python file containing the original code plus the test so that I just need to run the resulting file and i can see if the tests go through