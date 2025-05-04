import unittest

def kth(arr, k):
    pivot = arr[0]
    below = [x for x in arr if x < pivot]
    above = [x for x in arr if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if k < num_less:
        return kth(below, k)
    elif k >= num_lessoreq:
        return kth(above, k - num_lessoreq)
    else:
        return pivot

class TestKth(unittest.TestCase):
    def test_kth(self):
        self.assertEqual(kth([3, 2, 1, 5, 6, 4], 0), 1)
        self.assertEqual(kth([3, 2, 1, 5, 6, 4], 1), 2)
        self.assertEqual(kth([3, 2, 1, 5, 6, 4], 2), 3)
        self.assertEqual(kth([3, 2, 1, 5, 6, 4], 3), 4)
        self.assertEqual(kth([3, 2, 1, 5, 6, 4], 4), 5)

if __name__ == '__main__':
    unittest.main()