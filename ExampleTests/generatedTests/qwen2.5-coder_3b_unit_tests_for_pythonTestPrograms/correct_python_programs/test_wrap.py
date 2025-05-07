import unittest


def wrap(text, cols):
    lines = []
    while len(text) > cols:
        end = text.rfind(" ", 0, cols + 1)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)

    lines.append(text)
    return lines


class TestWrapFunction(unittest.TestCase):
    def test_wrap_short_text(self):
        self.assertEqual(
            wrap("This is a short test", 5), ["This is", "a short", "test"]
        )

    def test_wrap_long_text_with_spaces(self):
        text = "This is a very long text that should be wrapped into multiple lines. This is to test the wrap function."
        expected_output = [
            "This is a very",
            "long text that",
            "should be wrapped",
            "into multiple",
            "lines. This is",
            "to test the",
            "wrap function.",
        ]
        self.assertEqual(wrap(text, 10), expected_output)

    def test_wrap_long_text_without_spaces(self):
        text = "Thisisthelongertextthatshouldbewrappedintomultiplelines.Thisistotestthewrapfunction."
        expected_output = [
            "Thisisthelong",
            "textthatshouldb",
            "ewrappedintomul",
            "tiplelines.Thisi",
            "snotwrap",
        ]
        self.assertEqual(wrap(text, 10), expected_output)

    def test_wrap_no_spaces(self):
        text = "NoSpacesHere"
        expected_output = ["NoSpaces", "Here"]
        self.assertEqual(wrap(text, 4), expected_output)

    def test_wrap_single_word(self):
        text = "SingleWord"
        expected_output = ["SingleWord"]
        self.assertEqual(wrap(text, 5), expected_output)


if __name__ == "__main__":
    unittest.main()
