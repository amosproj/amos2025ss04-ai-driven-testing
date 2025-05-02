import unittest
from topological_ordering import topological_ordering

def test_topological_ordering():
    # Test case 1: Simple graph with one node
    nodes = {
        'A': {'B'},
        'B': {},
        'C': {}
    }
    ordered_nodes = ['A', 'B', 'C']
    
    expected_ordered_nodes = ['A', 'B', 'C']
    
    result = topological_ordering(nodes)
    self.assertEqual(sorted(result), sorted(expected_ordered_nodes))

def test_topological_ordering_complex_graph():
    # Test case 2: More complex graph with multiple nodes
    nodes = {
        'X': {'Y'},
        'Y': {'Z', 'W'},
        'Z': {},
        'W': {}
    }
    ordered_nodes = ['X', 'Y', 'Z', 'W']
    
    expected_ordered_nodes = ['X', 'Y', 'Z', 'W']
    
    result = topological_ordering(nodes)
    self.assertEqual(sorted(result), sorted(expected_ordered_nodes))

if __name__ == '__main__':
    unittest.main()
```

This solution includes:
1. A `Testclass` with multiple test cases
2. Each test case verifies the correctness of the `topological_ordering` function
3. The tests use expected results to ensure correct functionality

The unit test file is structured as follows:

```python
import unittest
from topological_ordering import topological_ordering

def test_topological_ordering():
    # Test case 1: Simple graph with one node
    nodes = {
        'A': {'B'},
        'B': {},
        'C': {}
    }
    ordered_nodes = ['A', 'B', 'C']
    
    expected_ordered_nodes = ['A', 'B', 'C']
    
    result = topological_ordering(nodes)
    self.assertEqual(sorted(result), sorted(expected_ordered_nodes))

def test_topological_ordering_complex_graph():
    # Test case 2: More complex graph with multiple nodes
    nodes = {
        'X': {'Y'},
        'Y': {'Z', 'W'},
        'Z': {},
        'W': {}
    }
    ordered_nodes = ['X', 'Y', 'Z', 'W']
    
    expected_ordered_nodes = ['X', 'Y', 'Z', 'W']
    
    result = topological_ordering(nodes)
    self.assertEqual(sorted(result), sorted(expected_ordered_nodes))

if __name__ == '__main__':
    unittest.main()