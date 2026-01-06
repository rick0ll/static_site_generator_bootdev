import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode

from conversion import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        """Test conversione TextType.TEXT -> LeafNode senza tag"""
        node = TextNode("Testo normale", TextType.TEXT)
        leaf = text_node_to_html_node(node)

        self.assertIsNone(leaf.tag)
        self.assertEqual(leaf.value, "Testo normale")

    def test_bold(self):
        """Test conversione TextType.BOLD -> LeafNode tag 'b'"""
        node = TextNode("Testo grassetto", TextType.BOLD)
        leaf = text_node_to_html_node(node)

        self.assertEqual(leaf.tag, "b")
        self.assertEqual(leaf.value, "Testo grassetto")

    def test_italic(self):
        """Test conversione TextType.ITALIC -> LeafNode tag 'i'"""
        node = TextNode("Testo italico", TextType.ITALIC)
        leaf = text_node_to_html_node(node)

        self.assertEqual(leaf.tag, "i")
        self.assertEqual(leaf.value, "Testo italico")

    def test_code(self):
        """Test conversione TextType.CODE -> LeafNode tag 'code'"""
        node = TextNode("print('hello')", TextType.CODE)
        leaf = text_node_to_html_node(node)

        self.assertEqual(leaf.tag, "code")
        self.assertEqual(leaf.value, "print('hello')")

    def test_link(self):
        """Test conversione TextType.LINK -> LeafNode tag 'a'"""
        # Nota: Nel tuo codice attuale href è vuoto (""), quindi testiamo quello.
        node = TextNode("Clicca qui", TextType.LINK, "https://www.google.com")
        leaf = text_node_to_html_node(node)

        self.assertEqual(leaf.tag, "a")
        self.assertEqual(leaf.value, "Clicca qui")
        self.assertEqual(
            leaf.props, {"href": "https://www.google.com"}
        )  # Verifica comportamento attuale

    def test_image(self):
        """Test conversione TextType.IMAGE -> LeafNode tag 'img'"""
        node = TextNode("Descrizione immagine", TextType.IMAGE, "url_immagine.png")
        leaf = text_node_to_html_node(node)

        self.assertEqual(leaf.tag, "img")
        self.assertEqual(leaf.value, "")
        self.assertEqual(
            leaf.props, {"src": "url_immagine.png", "alt": "Descrizione immagine"}
        )

    def test_invalid_type(self):
        """Test errore se TextType non è valido"""

        # Creiamo un nodo con un tipo che non esiste nel match case
        # (Qui forziamo un valore fittizio se TextType è un Enum o stringa)
        class FakeNode:
            def __init__(self):
                self.text_type = "UNKNOWN_TYPE"
                self.text = "test"

        with self.assertRaises(AttributeError):
            text_node_to_html_node(FakeNode())


if __name__ == "__main__":
    unittest.main()
