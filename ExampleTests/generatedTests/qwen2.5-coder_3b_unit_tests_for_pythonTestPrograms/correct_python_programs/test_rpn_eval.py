import unittest


class TestRPN_Eval(unittest.TestCase):
    def test_empty_tokens(self):
        with self.assertRaises(Exception) as cm:
            rpn_eval([])
        self.assertEqual(str(cm.exception), "stack is empty")

    def test_single_number(self):
        self.assertEqual(rpn_eval([5.0]), 5.0)

    def test_single_operator(self):
        with self.assertRaises(Exception) as cm:
            rpn_eval(["+"])
        self.assertEqual(str(cm.exception), "single operator: +")

    def test_two_operands(self):
        self.assertEqual(rpn_eval([3, 4, "+"]), 7.0)

    def test_addition(self):
        self.assertEqual(rpn_eval([1, 2, 3, "+", "+"]), 6.0)

    def test_subtraction(self):
        self.assertEqual(rpn_eval([5, 3, "-", "-"]), 2.0)

    def test_multiplication(self):
        self.assertEqual(rpn_eval([4, 3, "*", "*"]), 72.0)

    def test_division(self):
        self.assertEqual(rpn_eval([16, 4, "/", "/"]), 1.0)

    def test_float_division(self):
        self.assertAlmostEqual(rpn_eval([5, 2, "/", "/"]), 1.25)


if __name__ == "__main__":
    unittest.main()
