def hanoi(height, start=1, end=3):
    steps = []
    if height > 0:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.append((start, end))
        steps.extend(hanoi(height - 1, helper, end))

    return steps


import unittest
from typing import List, Tuple

class TestHanoi(unittest.TestCase):
    def test_hanoi(self) -> None:
        self.assertEqual(
            hanoi(0),
            [],
            "For height 0, no moves should be made."
        )
        self.assertEqual(
            hanoi(1),
            [(1, 3)],
            "For height 1, the single disk should move from peg 1 to peg 3."
        )
        self.assertEqual(
            hanoi(2),
            [(1, 2), (1, 3), (2, 3)],
            "For height 2, the sequence of moves should be as follows: (1, 2), (1, 3), (2, 3)."
        )
        self.assertEqual(
            hanoi(3),
            [(1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3)],
            "For height 3, the sequence of moves should be as follows: (1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3)."
        )

if __name__ == '__main__':
    unittest.main()