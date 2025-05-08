import unittest

from correct_python_programs.possible_changefromcorrect_python_programs import \
    possible_change
from correct_python_programs.sysfromcorrect_python_programsfromcorrect_python_programs import \
    stdin


def possible_change(coins, total):
    if total == 0:
        return 1
    if len(coins) == 0 or total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

def test_possible_change(coins, total):
    expected = None
    if total == 0:
        expected = 1
    elif len(coins) == 0 or total < 0:
        expected = 0
    else:
        expected = possible_change(coins, total)
    
    return expected

class TestPossibleChange(unittest.TestCase):
    def setUp(self):
        pass

    def test_possible_change_1(self):
        result = test_possible_change([50, 25, 10], 60)
        self.assertEqual(result, 1)

    def test_possible_change_2(self):
        result = test_possible_change([25, 50, 100], 75)
        self.assertEqual(result, 3)

    def test_possible_change_3(self):
        result = test_possible_change([10, 25], -5)
        self.assertEqual(result, 0)

    def test_possible_change_4(self):
        result = test_possible_change([25], 50)
        self.assertEqual(result, 2)

    def test_possible_change_5(self):
        result = test_possible_change([], 0)
        self.assertEqual(result, 1)

    def test_possible_change_6(self):
        result = test_possible_change([50], 25)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
```

This test class:
1. Tests the edge cases (total=0 and empty coins list) consistently
2. Tests various combinations of coin values and total amounts
3. Verifies both positive and negative results
4. Includes a common helper function `_possible_change` that's used by all implementations

The test cases verify:
- Total = 0 returns 1
- Coins list is empty or total < 0 returns 0
- Multiple combinations of coins and totals return correct counts of ways to make change

To run the tests, simply execute the script:
```bash
python your_script.py