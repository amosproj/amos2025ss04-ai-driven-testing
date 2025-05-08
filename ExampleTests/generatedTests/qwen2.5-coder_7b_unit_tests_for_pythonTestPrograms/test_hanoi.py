import unittest


def hanoi(height, start=1, end=3):
    steps = []
    if height > 0:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.append((start, end))
        steps.extend(hanoi(height - 1, helper, end))

    return steps


class TestHanoi(unittest.TestCase):
    def test_hanoi_0(self):
        self.assertEqual(hanoi(0), [])

    def test_hanoi_1(self):
        self.assertEqual(hanoi(1), [(1, 3)])

    def test_hanoi_2(self):
        expected = [(1, 2), (1, 3), (2, 3)]
        self.assertEqual(hanoi(2), expected)

    def test_hanoi_3(self):
        expected = [(1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3)]
        self.assertEqual(hanoi(3), expected)


if __name__ == "__main__":
    unittest.main()
