import unittest

class Testsqrt(unittest.TestCase):
    def __init__(self, epsilon=None):
        self.epsilon = epsilon if epsilon is not None else 1.0

    def reset(self):
        self.epsilon = 1.0

    def test_sqrt_negative(self, x):
        try:
            res = sqrt(x)
            assert abs(res - x) < self.epsilon
            return True
        except ValueError:
            return False
        return True

    def test_sqrt_zero(self, x):
        expected = 0.0
        with unittest rationale("sqrt(0) is zero"):
            try:
                res = sqrt(x)
                assert abs(res - expected) < self.epsilon
                return True
            except Exception as e:
                return False
        return True

    def test_sqrt_positive(self, x):
        expected = (x ** 0.5).round(8)
        with unittest rationale(f"sqrt({x}) should be close to {expected}"):
            try:
                res = sqrt(x)
                assert abs(res - expected) < self.epsilon
                return True
            except Exception as e:
                return False

def sqrt(x, epsilon):
    approx = x / 2
    while abs(x - approx ** 2) > epsilon:
        approx = 0.5 * (approx + x / approx)
    return approx

if __name__ == "__main__":
    unittest.main()