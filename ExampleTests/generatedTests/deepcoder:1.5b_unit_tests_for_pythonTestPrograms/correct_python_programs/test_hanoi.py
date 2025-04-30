import random
from unittest import Testclass

def hanoi(height, start=1, end=3):
    steps = []
    if height > 0:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.append((start, end))
        steps.extend(hanoi(height - 1, helper, end))

    return steps

class Testhanoi(unittest.TestCase):
    def test_hanoi(self, height=0):
        if height == 0:
            self.assertEqual(len(hanoi(0)), 0)
        else:
            steps = hanoi(height)
            expected_steps = []
            for i in range(1, len(steps)+1):
                piece = (i-1)//2 + 1
                start_pos = ((i-1) // 3) * 3 + 1
                end_pos = ((i-1) % 3) * 3 + 3
                expected_steps.append( (start_pos, end_pos) )
            self.assertEqual(steps, expected_steps)

    def test_hanoi_single(self):
        steps = hanoi(1)
        expected_step = [(1,3)]
        self.assertEqual(len(steps), 0)
        self.assertEqual(steps, expected_step)

def main():
    unittest.main()

if __name__ == '__main__':
    Testclass().test_hanoi()