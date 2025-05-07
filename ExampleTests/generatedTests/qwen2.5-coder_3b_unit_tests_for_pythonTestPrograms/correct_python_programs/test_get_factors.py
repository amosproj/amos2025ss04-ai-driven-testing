import unittest


class TestGetFactors(unittest.TestCase):
    def test_get_factors_1(self):
        self.assertEqual(get_factors(1), [])

    def test_get_factors_2(self):
        self.assertEqual(get_factors(2), [2])

    def test_get_factors_3(self):
        self.assertEqual(get_factors(3), [3])

    def test_get_factors_4(self):
        self.assertEqual(get_factors(4), [2, 2])

    def test_get_factors_5(self):
        self.assertEqual(get_factors(5), [5])

    def test_get_factors_6(self):
        self.assertEqual(get_factors(6), [2, 3])

    def test_get_factors_7(self):
        self.assertEqual(get_factors(7), [7])

    def test_get_factors_8(self):
        self.assertEqual(get_factors(8), [2, 2, 2])

    def test_get_factors_9(self):
        self.assertEqual(get_factors(9), [3, 3])

    def test_get_factors_10(self):
        self.assertEqual(get_factors(10), [2, 5])

    def test_get_factors_16(self):
        self.assertEqual(get_factors(16), [2, 2, 2, 2])

    def test_get_factors_17(self):
        self.assertEqual(get_factors(17), [17])

    def test_get_factors_20(self):
        self.assertEqual(get_factors(20), [2, 2, 5])

    def test_get_factors_24(self):
        self.assertEqual(get_factors(24), [2, 2, 2, 3])


# Run the tests
if __name__ == "__main__":
    unittest.main()
