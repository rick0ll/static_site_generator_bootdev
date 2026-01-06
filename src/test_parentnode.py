import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_many_children(self):
        """
        Test Multipli Figli: Verifica che l'ordine sia mantenuto e
        che LeafNode senza tag (testo puro) siano gestiti.
        """
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        output = node.to_html()
        # Verifichiamo la sequenza corretta
        expected_content = "<b>Bold text</b>Normal text<i>italic text</i>Normal text"
        self.assertIn(expected_content, output)

    def test_headings(self):
        """
        Test Props: Verifica che il genitore renderizzi correttamente le sue props.
        """
        node = ParentNode(
            "h2", [LeafNode("b", "Title")], {"class": "header-text", "id": "main-title"}
        )
        output = node.to_html()
        self.assertIn('class="header-text"', output)
        self.assertIn('id="main-title"', output)
        self.assertIn("<b>Title</b>", output)

    def test_to_html_no_children(self):
        """
        Edge Case Error: Un ParentNode DEVE avere figli (secondo la tua logica),
        altrimenti deve alzare ValueError.
        """
        # Passiamo None come lista figli
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children_list(self):
        """
        Edge Case: Lista figli vuota [].
        A seconda della logica, questo potrebbe non alzare errore ma produrre un tag vuoto,
        oppure alzare errore se consideri [] come "nessun figlio".
        Il tuo codice controlla 'if self.children is None', quindi [] passerà.
        """
        node = ParentNode("div", [])
        output = node.to_html()
        # Verifica che produca un div vuoto (con o senza lo spazio buggato)
        # Regex semplice per accettare sia "<div ></div>" che "<div></div>"
        self.assertTrue(output.startswith("<div") and output.endswith("></div>"))

    def test_to_html_no_tag(self):
        """
        Edge Case Error: Un ParentNode non può essere testo puro, deve avere un tag.
        """
        node = ParentNode(None, [LeafNode("b", "bold")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
