<<<<<<< SEARCH
=======
import unittest
from shortest_paths import shortest_paths

class TestShortestPaths(unittest.TestCase):
    def test_shortest_paths(self):
        # Test case 1: Simple path graph
        weight_by_edge = {
            ('A', 'B'): 2,
            ('B', 'C'): 3,
            ('A', 'D'): 4
        }
        expected_output = {'A':0, 'B':2, 'C':5, 'D':4}
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result['A'], 0.0)
        self.assertEqual(result['B'], 2.0)
        self.assertEqual(result['C'], 5.0)
        self.assertEqual(result['D'], 4.0)

        # Test case 2: Multiple paths
        weight_by_edge = {
            ('A', 'B'): 1,
            ('A', 'D'): 4,
            ('B', 'C'): 2,
            ('B', 'D'): 3,
            ('C', 'D'): 1
        }
        expected_output = {'A':0, 'B':1, 'C':3, 'D':3}
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result['A'], 0.0)
        self.assertEqual(result['B'], 1.0)
        self.assertEqual(result['C'], 3.0)
        self.assertEqual(result['D'], 3.0)

        # Test case 3: All edges have same weight
        weight_by_edge = {
            ('A', 'B'):2,
            ('B', 'C'):2,
            ('C', 'D'):2
        }
        expected_output = {'A':0, 'B':2, 'C':4, 'D':6}
        result = shortest_paths('A', weight_by_edge)
        self.assertEqual(result['A'], 0.0)
        self.assertEqual(result['B'], 2.0)
        self.assertEqual(result['C'], 4.0)
        self.assertEqual(result['D'], 6.0)

if __name__ == '__main__':
    unittest.main()
>>>>>>> REPLACE
```

The test class includes:
1. A test case for a simple linear graph
2. A test case with multiple possible paths between nodes
3. A test case where all edges have the same weight

To run the tests, use:
```bash
python -m unittest test_shortestpaths.py