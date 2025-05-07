def hanoi(height, start=1, end=3):
    steps = []
    if height > 0:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.append((start, end))
        steps.extend(hanoi(height - 1, helper, end))

    return steps


import unittest


class TestHanoi(unittest.TestCase):
    def test_hanoi_moves(self, height):
        expected_moves = (2**height) - 1
        actual_moves = len(hanoi(height))
        self.assertEqual(
            expected_moves,
            actual_moves,
            f"Number of moves for height {height} should be {expected_moves}",
        )

    def test_hanoi_moves_between(self, height):
        steps = hanoi(height)
        valid_pegs = {1, 2, 3}
        for move in steps:
            if not (move[0] in valid_pegs and move[1] in valid_pegs):
                self.fail(
                    f"Invalid peg move found: moving from {move[0]} to {move[1]}"
                )

    def test_hanoi_move_consistency(self, height):
        steps = hanoi(height)
        seen_moves = set()
        for move in steps:
            if move in seen_moves or (move[0], move[1]) == (move[1], move[0]):
                self.fail(f"Duplicate or invalid move detected: {move}")
            seen_moves.add(move)


if __name__ == "__main__":
    unittest.main()
