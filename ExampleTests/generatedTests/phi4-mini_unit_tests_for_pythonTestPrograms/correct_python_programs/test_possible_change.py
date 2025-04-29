import unittest

def possible_change(coins, total):
    if total == 0:
        return 1
    if not coins or total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

class TestPossibleChange(unittest.TestCase):

    def test_possible_change_with_total_zero(self):
        self.assertEqual(possible_change([1, 2], 0), 1)
    
    def test_possible_change_negative_total(self):
        coins = [5]
        with self.assertRaises(AssertionError):  # Check if it handles negative total correctly
            possible_change(coins, -3)

    def test_possible_change_empty_coins_no_positive_total(self):
        self.assertEqual(possible_change([], 100), 0)
    
    def test_possible_change_non_negative_total_with_coins(self):
        coins = [1]
        for i in range(101):  # Total from 0 to 100
            result = possible_change([coins], i)
            if (i % len(coins)) == 0:
                self.assertEqual(result, pow(len(coins), i))
            else:  # For non-multiples of coin value length
                expected_result_1_coin = int(i / coins[0]) + result // powers_of_two[i - (len(coins) * (i // len(coins))) % len(coins)]
                self.assertEqual(result, expected_result_1_coin)

    def test_possible_change_with_positive_total(self):
        for total in [5, 10]:
            with self.subTest(total=total):  # Subtests to check different totals
                coins = list(range(1, min(total + 2)))
                result_expected = possible_change(coins, total)
                actual_result = possible_change([coins], total)

                if len(coins) == (len(possibilities[total][0]) // 2):
                    possibilities[(total, coins)] = [result for i in range(len(coin), results_total[i] + result)]

if __name__ == '__main__':
    unittest.main()
```

To run this test suite with a standard Python interpreter:
- Save the code above into `test_possible_change.py`.
- Run it using: 

```bash
python -m unittest test_possible_change.py