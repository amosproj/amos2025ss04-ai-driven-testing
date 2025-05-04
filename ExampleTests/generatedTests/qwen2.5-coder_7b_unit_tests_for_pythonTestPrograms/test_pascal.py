import unittest

def pascal(n):
    rows = [[1]]
    for r in range(1, n):
        row = []
        for c in range(0, r + 1):
            upleft = rows[r - 1][c - 1] if c > 0 else 0
            upright = rows[r - 1][c] if c < r else 0
            row.append(upleft + upright)
        rows.append(row)

    return rows

class TestPascalTriangle(unittest.TestCase):
    def test_pascal_0(self):
        self.assertEqual(pascal(0), [])

    def test_pascal_1(self):
        self.assertEqual(pascal(1), [[1]])

    def test_pascal_2(self):
        self.assertEqual(pascal(2), [[1], [1, 1]])

    def test_pascal_3(self):
        self.assertEqual(pascal(3), [[1], [1, 1], [1, 2, 1]])

    def test_pascal_4(self):
        self.assertEqual(pascal(4), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]])

if __name__ == '__main__':
    unittest.main()