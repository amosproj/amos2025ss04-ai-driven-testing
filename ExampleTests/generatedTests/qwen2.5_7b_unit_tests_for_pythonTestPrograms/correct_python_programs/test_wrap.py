def wrap(text, cols):
    lines = []
    while len(text) > cols:
        end = text.rfind(' ', 0, cols + 1)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)

    lines.append(text)
    return lines


import unittest

class TestWrapFunction(unittest.TestCase):
    
    def test_wrap(self):
        self.assertEqual(wrap("The quick brown fox jumps over the lazy dog", 10), 
                         ["The quick ", "brown fox ", "jumps over", "the lazy d", "og"])
        
        self.assertEqual(wrap("The quick brown fox jumps over the lazy dog", 20),
                         ["The quick brown fox jumps", "over the lazy dog"])

        self.assertEqual(wrap("", 10), [""])
        
        self.assertEqual(wrap("a", 1), ["a"])
        
        self.assertEqual(wrap("a", 2), ["a"])
        
        self.assertEqual(wrap("ab", 1), ["a", "b"])


if __name__ == '__main__':
    unittest.main()