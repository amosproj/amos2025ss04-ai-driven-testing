import unittest

class TestSqrtFunction(unittest.TestCase):
    def test_sqrt(self):
        self.assertAlmostEqual(sqrt(4, 0.0001), 2)
        self.assertAlmostEqual(sqrt(9, 0.0001), 3)
        self.assertAlmostEqual(sqrt(0.25, 0.0001), 0.5)
        self.assertAlmostEqual(sqrt(2, 0.0001), 1.41421356237)
        self.assertAlmostEqual(sqrt(10, 0.0001), 3.16227766017)

if __name__ == '__main__':
    unittest.main()