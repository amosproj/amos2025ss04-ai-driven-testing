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


import unittest


class TestPascalTriangle(unittest.TestCase):
    def test_pascal_triangle(self):
        self.assertEqual(pascal(1), [[1]])
        self.assertEqual(pascal(2), [[1], [1, 1]])
        self.assertEqual(pascal(3), [[1], [1, 1], [1, 2, 1]])
        self.assertEqual(pascal(4), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]])


if __name__ == '__main__':
    unittest.main()
```

To run this script, save it to a file (e.g., `test_pascal.py`) and execute the following command in your terminal:

```sh
python test_pascal.py