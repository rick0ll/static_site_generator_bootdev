import unittest

# Assicurati che il file con le funzioni si chiami 'get_markdown_anchors.py'
from get_markdown_anchors import extract_markdown_images, extract_markdown_links


class TestMarkdownAnchors(unittest.TestCase):
    # --- TEST PER LE IMMAGINI ---

    def test_extract_markdown_images(self):
        # Caso base: una singola immagine
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        # Caso: immagini multiple
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_none(self):
        # Caso: nessuna immagine presente
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    # --- TEST PER I LINK ---

    def test_extract_markdown_links(self):
        # Caso base: un singolo link
        text = "This is text with a [link](https://www.google.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_links_multiple(self):
        # Caso: link multipli
        text = "Here is a link to [boot.dev](https://www.boot.dev) and [youtube](https://www.youtube.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("boot.dev", "https://www.boot.dev"),
            ("youtube", "https://www.youtube.com"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_none(self):
        # Caso: nessun link presente
        text = "Just plain text without anchors"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_ignores_images(self):
        # Edge Case: I link non devono catturare le immagini (che iniziano con !)
        # Testiamo una stringa che ha SIA un link CHE un'immagine
        text = "This is a link [to boot dev](https://www.boot.dev) and this is an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        matches = extract_markdown_links(text)

        # Ci aspettiamo che trovi SOLO il link "to boot dev", ignorando completamente "obi wan"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(expected, matches)


if __name__ == "__main__":
    unittest.main()
