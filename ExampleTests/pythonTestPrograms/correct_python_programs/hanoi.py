"""Module for solving the Tower of Hanoi puzzle.

This module implements a recursive algorithm to solve the classic Tower of Hanoi
problem, which involves moving disks of different sizes between three pegs
while following specific rules.
"""


def hanoi(height, start=1, end=3):
    """Generate a sequence of moves to solve the Tower of Hanoi puzzle.

    Uses a recursive approach to determine the optimal sequence of moves
    to transfer a tower of disks from the start peg to the end peg.

    Args:
        height: Number of disks in the tower
        start: Peg number (1-3) where the tower starts (default: 1)
        end: Peg number (1-3) where the tower should end up (default: 3)

    Returns:
        list: A list of move tuples (from_peg, to_peg) representing
              the sequence of moves to solve the puzzle
    """
    steps = []
    if height > 0:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.append((start, end))
        steps.extend(hanoi(height - 1, helper, end))

    return steps
