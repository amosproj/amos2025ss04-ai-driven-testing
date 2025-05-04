import unittest

class TestShortestPathLengths(unittest.TestCase):
    def test_shortest_path_lengths(self):
        n = 4
        length_by_edge = {(0, 1): 5, (0, 3): 9, (1, 2): 6, (1, 3): 8, (2, 3): 7}
        
        result = shortest_path_lengths(n, length_by_edge)
        
        expected_result = {
            (0, 0): 0,
            (0, 1): 5,
            (0, 2): float('inf'),
            (0, 3): 9,
            (1, 0): float('inf'),
            (1, 1): 0,
            (1, 2): 6,
            (1, 3): 8,
            (2, 0): float('inf'),
            (2, 1): 6,
            (2, 2): 0,
            (2, 3): 7,
            (3, 0): 9,
            (3, 1): 8,
            (3, 2): 7,
            (3, 3): 0
        }
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()