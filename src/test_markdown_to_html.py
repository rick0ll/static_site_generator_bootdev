import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1><h2>Heading 2</h2></div>")

    def test_lists(self):
        # Testiamo sia ordinata che non ordinata
        md = """
- Unordered 1
- Unordered 2

1. Ordered 1
2. Ordered 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<ul><li>Unordered 1</li><li>Unordered 2</li></ul>"
            "<ol><li>Ordered 1</li><li>Ordered 2</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_blockquote(self):
        md = """
> First line of quote
> Second line of quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Assumendo che il tuo parser unisca le righe con uno spazio
        self.assertEqual(
            html,
            "<div><blockquote>First line of quote Second line of quote</blockquote></div>",
        )

    def test_inline_elements_inside_blocks(self):
        # Verifica che il grassetto, corsivo e link funzionino dentro i blocchi
        md = "This is **bold** and _italic_ and a [link](https://boot.dev)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is <b>bold</b> and <i>italic</i> and a <a href="https://boot.dev">link</a></p></div>',
        )

    def test_images_inside_blocks(self):
        md = "This is an ![image](url.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, '<div><p>This is an <img src="url.png" alt="image"></img></p></div>'
        )

    def test_full_document_structure(self):
        # Un test complesso che simula un documento reale
        md = """
# Main Header

This is a paragraph with **bold** text.

* List item 1
* List item 2

```
print("Code")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None

        expected = (
            "<div>"
            "<h1>Main Header</h1>"
            "<p>This is a paragraph with <b>bold</b> text.</p>"
            "<ul><li>List item 1</li><li>List item 2</li></ul>"
            '<pre><code>print("Code")</code></pre>'
            "</div>"
        )
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
