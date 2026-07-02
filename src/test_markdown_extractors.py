import unittest
from markdown_extractors import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images(self):

        result = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            result,
        )

    def test_extract_markdown_links(self):

        result = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            result,
        )

    def test_extract_markdown_links_ignores_images(self):
        
        result = extract_markdown_links(
            "This has an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [boot dev](https://www.boot.dev)"
        )

        self.assertEqual(
            [("boot dev", "https://www.boot.dev")], 
            result,
        )

    def test_extract_markdown_images_ignores_links(self):
        
        result = extract_markdown_images(
            "This has a link [boot dev](https://www.boot.dev) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        )

        self.assertEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
            result,
        )

if __name__ == "__main__":
    unittest.main()