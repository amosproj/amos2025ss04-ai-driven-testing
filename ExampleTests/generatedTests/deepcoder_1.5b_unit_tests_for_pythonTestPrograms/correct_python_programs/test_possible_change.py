import unittest

class TestpossibleChange(unittest.TestCase):
    def test_possible_change(self, coins, total):
        # Implementing unit tests for possible_change
        pass

if __name__ == "__main__":
    unittest.main()
```

现在，我将生成一个包含所有已定义函数和测试类的Python文件。这个文件将包括原始代码以及测试类。

```python
def possible_change(coins, total):
    if total == 0:
        return 1
    if not coins or total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

class TestpossibleChange(unittest.TestCase):
    def test_possible_change(self, coins, total):
        result = possible_change(coins, total)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()