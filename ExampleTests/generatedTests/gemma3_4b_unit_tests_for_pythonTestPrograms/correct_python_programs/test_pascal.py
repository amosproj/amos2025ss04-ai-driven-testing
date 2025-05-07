class Pascal:
    def pascal(self, n):
        rows = [[1]]
        for r in range(1, n):
            row = []
            for c in range(0, r + 1):
                upleft = rows[r - 1][c - 1] if c > 0 else 0
                upright = rows[r - 1][c] if c < r else 0
                row.append(upleft + upright)
            rows.append(row)

        return rows


import unittest


class TestPascal(unittest.TestCase):
    def test_pascal_0(self):
        pascal_object = Pascal()
        expected = [[1]]
        self.assertEqual(pascal_object.pascal(0), expected)

    def test_pascal_1(self):
        pascal_object = Pascal()
        expected = [[1]]
        self.assertEqual(pascal_object.pascal(1), expected)

    def test_pascal_2(self):
        pascal_object = Pascal()
        expected = [[1], [1, 1], [1, 2, 1]]
        self.assertEqual(pascal_object.pascal(2), expected)

    def test_pascal_3(self):
        pascal_object = Pascal()
        expected = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
        self.assertEqual(pascal_object.pascal(3), expected)

    def test_pascal_4(self):
        pascal_object = Pascal()
        expected = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
        self.assertEqual(pascal_object.pascal(4), expected)


if __name__ == "__main__":
    unittest.main()
