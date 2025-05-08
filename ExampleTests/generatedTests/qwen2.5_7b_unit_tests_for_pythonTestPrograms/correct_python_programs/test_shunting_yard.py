def shunting_yard(tokens):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    rpntokens = []
    opstack = []
    for token in tokens:
        if isinstance(token, int):
            rpntokens.append(token)
        else:
            while opstack and precedence[token] <= precedence[opstack[-1]]:
                rpntokens.append(opstack.pop())
            opstack.append(token)

    while opstack:
        rpntokens.append(opstack.pop())

    return rpntokens


import unittest


class TestShuntingYard(unittest.TestCase):
    def test_shunting_yard(self):
        self.assertEqual(
            shunting_yard([3, "+", 4, "*", 2]), [3, 4, 2, "*", "+"]
        )
        self.assertEqual(
            shunting_yard(["(", 5, "-", 7, ")", "/", 3]), [5, 7, "-", 3, "/"]
        )
        self.assertEqual(
            shunting_yard([10, "/", 5, "+", 2, "*", 4]),
            [10, 5, "/", 2, 4, "*", "+"],
        )


if __name__ == "__main__":
    unittest.main()
