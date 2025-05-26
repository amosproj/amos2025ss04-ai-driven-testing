import unittest
def add_numbers(a, b):
    # Your original function goes here
    return a + b

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-3, -4), 7)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(1.23, 4.56), 5.79)
        self.assertAlmostEqual(add_numbers(-0.12, 0.23), 0.11)

if __name__ == '__main__':
    unittest.main()


In this example, the `TestAddNumbers` class is a test case that includes two methods: `test_add_integers` and `test_add_floats`. Each method tests a specific scenario (adding integers or floating-point numbers). The `self.assertEqual` and `self.assertAlmostEqual` functions check if the expected and actual outputs match, and `unittest.main()` runs all the tests.