import unittest

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


class TestWrapFunction(unittest.TestCase):

    def test_wrap_with_space(self):
        self.assertEqual(wrap("This is a short sentence", 10), ["This is ", "a short s"])

    def test_wrap_without_extra_spaces(self):
        self.assertEqual(wrap("NoSpacesNeededHereButLongTextThatExceedsTheLimitOfCharactersAllowedInEachLineForTestingPurposesOnlyBecauseWeWantToEnsureItWorksAsExpectedBySplittingIntoMultipleLines", 50), 
                         ["NoSpacesNeededHereButLongT", "ext thatExceedsTh"])


if __name__ == '__main__':
    unittest.main()