import unittest

def pascal(n):
    rows = [[1]]
    for r in range(1, n):
        row = []
        for c in range(0, r + 1):
            upleft = rows[r - 1][c - 1] if c > 0 else 0
            upright = rows[r - 1][c] if c < len(rows[r-1]) else 0
            row.append(upleft + upright)
        rows.append(row)

    return rows

class PascalTest(unittest.TestCase):
    def test_pascal_with_n_none(self):
        self.assertIsNone(pascal(None))
    
    def test_pascal_n_0(self):
        result = pascal(0)
        self.assertEqual(result, None)
    
    def test_pascal_n_1(self):
        result = pascal(1)
        self.assertEqual(result, [[1]])
    
    def test_pascal_n_2(self):
        expected = [[1], [1, 1]]
        self.assertListEquals(pascal(2), expected)
    
    def test_pascal_n_5(self):
        expected_row_4 = [1, 3, 3, 1]
        self.assertListEquals(pascal(5)[4], expected_row_4)
    
    def test_pascal_n_10(self):
        expected_row_9 = [1, 8, 28, 56, 70, 56, 28, 8, 1]
        self.assertListEquals(pascal(10)[9], expected_row_9)

if __name__ == '__main__':
    unittest.main()