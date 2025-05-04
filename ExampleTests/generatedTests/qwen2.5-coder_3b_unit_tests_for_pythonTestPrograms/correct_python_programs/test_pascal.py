import unittest

class TestPascal(unittest.TestCase):
    def test_pascal(self):
        self.assertEqual(pascal(0), [[1]])
        self.assertEqual(pascal(1), [[1], [1, 1]])
        self.assertEqual(pascal(2), [[1], [1, 1], [1, 2, 1]])
        self.assertEqual(pascal(3), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]])

    def test_pascal_zero(self):
        self.assertEqual(pascal(0), [[1]])

    def test_pascal_one(self):
        self.assertEqual(pascal(1), [[1], [1, 1]])

    def test_pascal_two(self):
        self.assertEqual(pascal(2), [[1], [1, 1], [1, 2, 1]])

    def test_pascal_three(self):
        self.assertEqual(pascal(3), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]])

if __name__ == '__main__':
    unittest.main()