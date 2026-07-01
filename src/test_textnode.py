import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Goodbye", TextType.TEXT)

        self.assertNotEqual(node1, node2)

    def test_not_eq_text_type(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.BOLD)

        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("BootDev", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("BootDev", TextType.LINK, "https://www.boot.dev/dashboard")

        self.assertNotEqual(node1, node2)
    
    def test_eq_url_none(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT)

        self.assertEqual(node1, node2)

    def test_not_eq_none_url(self):
        node1 = TextNode("BootDev", TextType.LINK)
        node2 = TextNode("BootDev", TextType.LINK, "https://www.boot.dev")

        self.assertNotEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_text_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_text_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_text_link(self):
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
    
    def test_text_img(self):
        node = TextNode("An image", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "An image"})

    def test_invalid_text(self):
        node = TextNode("Hello", None)

        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()