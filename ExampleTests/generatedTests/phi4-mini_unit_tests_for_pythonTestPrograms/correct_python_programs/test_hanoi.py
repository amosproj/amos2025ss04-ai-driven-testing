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

    def test_hanoi_basic(self):
        self.assertEqual(hanoi(2), [(1, 3), (1, 2)])

    def test_hanoi_larger_size(self):
        result = hanoi(4)
        expected_steps = [
            (1, 'end'),
            (1, 'middle'),
            ('start', 'end'),
            (1, 'middle'),
            ('start', 'mid-middle'),
            ('mid-start', 'end'),
            ('mid-middle', 'mid-end'),
            ('mid-middle', 3),
        ]
        self.assertEqual(result[0], expected_steps)

    def test_hanoi_empty(self):
        result = hanoi(0)
        self.assertEqual([], result)


if __name__ == '__main__':
    unittest.main()