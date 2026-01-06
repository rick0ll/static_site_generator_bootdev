import unittest
from leafnode import LeafNode  # Assumiamo che il file si chiami htmlnode.py


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_multiple_props(self):
        """
        Test 1: Verifica il rendering con tag e attributi multipli.
        Controlla che props_to_html formatti correttamente senza spazi finali extra
        e che LeafNode assembli il tutto.
        """
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode("a", "Clicca qui!", props)

        # HTMLNode genera: 'href="val" target="val"' (senza spazio finale)
        # LeafNode aggiunge: '<a ' + props + '>'
        expected_output = (
            '<a href="https://www.google.com" target="_blank">Clicca qui!</a>'
        )

        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_no_tag_text_only(self):
        """
        Test 2: Verifica il caso di nodo di testo puro (tag=None).
        Questo è fondamentale per il rendering del testo semplice all'interno dell'HTML.
        """
        node = LeafNode(None, "Questo è un testo semplice.")

        # Deve restituire il valore raw senza decorazioni HTML
        self.assertEqual(node.to_html(), "Questo è un testo semplice.")

    def test_validation_error_no_value(self):
        """
        Test 3: Verifica la robustezza (Error Handling).
        Un nodo foglia (LeafNode) non può esistere senza un valore, deve alzare ValueError.
        """
        # Passiamo None come valore
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
