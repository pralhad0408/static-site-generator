import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        md = "# This is a title"
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_h1_after_blocks(self):
        md = """
This is paragraph text

# This is a title
""".strip()
        
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_missing_space_after_h1(self):
        md = "#This is a title"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_h2_only(self):
        md = "## This is a title"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_no_heading(self):
        md = "This is a paragraph"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_multiple_h1_headers(self):
        md = """
# This is a title

Some text

# This is another title
""".strip()
        
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_h1_after_h2_h3_headers(self):
        md = """
### H3

## H2

# Finally H1
""".strip()
        
        title = extract_title(md)
        self.assertEqual(title, "Finally H1")

if __name__ == "__main__":
    unittest.main()