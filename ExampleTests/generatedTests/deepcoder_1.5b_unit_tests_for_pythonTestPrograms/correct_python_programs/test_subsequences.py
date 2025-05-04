import unittest
from .subsequences import subsequences

class Testsubsequences(unittest.TestCase):
    def test_subsequences(self):
        # Test case 1: k=2, a=1, b=3
        self.assertEqual(subsequences(1, 3, 2), [[1,2], [1,3], [2,3]])
        
        # Test case 2: k=0, a=5, b=10
        self.assertEqual(subsequences(5, 10, 0), [[]])
        
        # Test case 3: k=3, a=4, b=6
        self.assertEqual(subsequences(4, 6, 3), [[4,5,6]])

if __name__ == "__main__":
    unittest.main()