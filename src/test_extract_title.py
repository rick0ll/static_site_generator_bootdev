import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_get_title(self):
        markdown = "# title\nother stuff\n\n##title two "
        result = extract_title(markdown)

        expected = "title"
        self.assertEqual(result, expected)

    def test_exception_get_title(self):
        markdown = "## title\nother stuff\n\n##title two "

        with self.assertRaises(ValueError):
            result = extract_title(markdown)
            print(result)
