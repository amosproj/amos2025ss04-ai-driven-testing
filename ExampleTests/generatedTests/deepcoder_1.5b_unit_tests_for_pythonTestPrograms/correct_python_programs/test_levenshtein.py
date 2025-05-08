import unittest


class Levenshteine:
    def levenshtein(self, source, target):
        if source == '' or target == '':
            return len(source) or len(target)
        
        if source[0] == target[0]:
            return self.levenshtein(source[1:], target[1:])
        else:
            return 1 + min(
                self.levenshtein(source, target[1]),
                self.levenshtein(source[1], target[1:]),
                self.levenshtein(source[1], target)
            )

class TestLevenshteine(unittest.TestCase):
    def test_levenshtein(self):
        # Test case 1: One string is empty
        self.assertEqual(self.levenshtein('hello', ''), len('hello'))
        
        # Test case 2: All characters match except for some mismatches
        self.assertEqual(self.levenshtein('abc', 'abd'), 1)
        
        # Test case 3: Edge cases
        self.assertEqual(self.levenshtein('', ''), 0)  # Should return len(source) or len(target)
            
    if __name__ == '__main__':
        unittest.main()