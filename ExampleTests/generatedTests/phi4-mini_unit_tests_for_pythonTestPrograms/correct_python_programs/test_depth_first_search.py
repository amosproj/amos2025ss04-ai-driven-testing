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

class TestDepthFirstSearch(unittest.TestCase):
    
    def setUp(self):
        self.start = "A"
        self.goal = ("D", {"successors": ["B", "C"]})
        self.graph = {
            'A': {'value': None, 'successors': []},
            'B': {'value': ('X', {}), 'successors': []},
            'C': {'value': ('Y', {})}, 
            'D': {'value': ('Z', {"successors": ["B", "C"]})}
        }
    
    def test_search_success(self):
        self.graph['A'].successors = [self.graph["B"], self.graph["C"]]
        result = depth_first_search("A", self.goal)
        self.assertTrue(result)

    def test_no_path_exists(self):
        del self.graph['D']
        with self.assertRaises(KeyError):  # Assuming KeyError if the node is missing
            _ = depth_first_search("B", "Z")

if __name__ == '__main__':
    unittest.main()