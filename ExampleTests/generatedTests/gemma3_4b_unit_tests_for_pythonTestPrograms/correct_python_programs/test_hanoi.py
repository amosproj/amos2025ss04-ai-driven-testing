def hanoi(height, start=1, end=3):
    steps = []
    if height > 0:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.append((start, end))
        steps.extend(hanoi(height - 1, helper, end))

    return steps


# Please generate a test class with unit tests for the above code using unittest. Return a python file containing the original code plus the test so that I just need to run the resulting file and i can see if the tests go through
import unittest


class TestHanoi(unittest.TestCase):
    def test_hanoi_1_disk(self):
        expected_steps = [(1, 3)]
        self.assertEqual(hanoi(1), expected_steps)

    def test_hanoi_2_disks(self):
        expected_steps = [
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
        ]
        self.assertEqual(hanoi(2), expected_steps)

    def test_hanoi_3_disks(self):
        expected_steps = [
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 1),
            (2, 3),
            (1, 3),
        ]
        self.assertEqual(hanoi(3), expected_steps)


if __name__ == "__main__":
    unittest.main()
