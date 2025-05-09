 # Unit Test for add_numbers function in Python

   ```python
   import unittest
   from your_module import add_numbers

   class TestAddNumbers(unittest.TestCase):
       def test_add_integers(self):
           self.assertEqual(add_numbers(2, 3), 5)
           self.assertEqual(add_numbers(-1, 1), 0)
           self.assertEqual(add_numbers(0, 1), 1)
           self.assertEqual(add_numbers(-1, -1), 0)

       def test_add_floats(self):
           self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
           self.assertAlmostEqual(add_numbers(0.3, 0.2), 0.5)
           self.assertAlmostEqual(add_numbers(-0.1, 0.1), 0.0)

       def test_mixed_types(self):
           self.assertEqual(add_numbers(1, 2.5), 3.5)
           self.assertEqual(add_numbers(-1, -2.5), -3.5)
           self.assertRaises(TypeError, add_numbers, "a", 2)

   if __name__ == '__main__':
       unittest.main()
   ```

   This unit test file checks the function for various scenarios such as adding integers, floating-point numbers, mixed types, and edge cases like zero sum. The `assertAlmostEqual` is used for comparing floating-point values with a small error tolerance due to rounding issues in float arithmetic. The `assertRaises` ensures that the function raises an error when given invalid inputs.