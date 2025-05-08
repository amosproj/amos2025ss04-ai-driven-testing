import unittest


class TestHanoi(unittest.TestCase):
    def test_hanoi(self):
        # Test case 1: Moving one disk
        self.assertEqual(hanoi(1), [(1, 3)])

        # Test case 2: Moving two disks
        expected_steps = [(1, 2), (1, 3), (2, 3)]
        self.assertEqual(hanoi(2), expected_steps)

        # Test case 3: Moving three disks
        expected_steps = [
            (1, 3),
            (1, 2),
            (3, 2),
            (1, 3),
            (2, 1),
            (2, 3),
            (1, 3),
        ]
        self.assertEqual(hanoi(3), expected_steps)

        # Test case 4: Edge case with no disks
        self.assertEqual(hanoi(0), [])


if __name__ == "__main__":
    unittest.main()
