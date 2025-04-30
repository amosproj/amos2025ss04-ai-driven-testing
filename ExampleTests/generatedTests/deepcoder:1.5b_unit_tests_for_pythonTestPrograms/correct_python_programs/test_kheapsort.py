import heapq
import unittest

def kheapsort(arr, k):
    heap = arr[:k]
    heapq.heapify(heap)
    
    for x in arr[k:]:
        yield heapq.heappushpop(heap, x)
        
    while heap:
        yield heapq.heappop(heap)

class TestKheapsort(unittest.TestCase):

    def test_kheapsort(self, arr, k):
        sorted_arr = kheapsort(arr, k)
        self.assertEqual(sorted_arr, list(arr) if k == len(arr) else None)

if __name__ == '__main__':
    with open('test_kheapsort.py', 'r') as f:
        original_code = f.read()
    
    with unittest.createTestClass("TestKheapsort") as test_class:
        test_class.addFunction(kheapsort)
        
        result = unittest.run(test_class, None, None, None)