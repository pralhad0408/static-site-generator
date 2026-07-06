import unittest

from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""".strip()
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
""".strip()
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_heading(self):
        md = """
# This is h1 heading

## This is h2 heading

### This is h3 heading

#### This is h4 heading

##### This is h5 heading

###### This is h6 heading
""".strip()
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is h1 heading</h1><h2>This is h2 heading</h2><h3>This is h3 heading</h3><h4>This is h4 heading</h4><h5>This is h5 heading</h5><h6>This is h6 heading</h6></div>"
        )

    def test_quote(self):
        md = """
> This is a quote
""".strip()
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- This is the first item
- This is the second item
- This is the third item
""".strip()
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is the first item</li><li>This is the second item</li><li>This is the third item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. This is the first item
2. This is the second item
3. This is the third item
""".strip()
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the first item</li><li>This is the second item</li><li>This is the third item</li></ol></div>"
        )

    def test_full_document(self):
        md = """
# My Page

This is a **bold** paragraph with a [link](https://www.boot.dev).

> This is a quote

- Apple
- Banana

1. First
2. Second

```
print("Hello")
```
""".strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>My Page</h1>"
            "<p>This is a <b>bold</b> paragraph with a "
            "<a href=\"https://www.boot.dev\">link</a>.</p>"
            "<blockquote>This is a quote</blockquote>"
            "<ul><li>Apple</li><li>Banana</li></ul>"
            "<ol><li>First</li><li>Second</li></ol>"
            "<pre><code>print(\"Hello\")</code></pre>"
            "</div>"
        )

if __name__ == "__main__":
    unittest.main()