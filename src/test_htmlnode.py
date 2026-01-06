import unittest
from leafnode import LeafNode
from htmlnode import HTMLNode


# Assumendo che la tua classe sia nello stesso file o importata correttamente
class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        """Verifica che i dizionari di proprietà vengano convertiti correttamente in stringhe HTML"""
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag="a", props=props)
        # Nota: nel tuo codice attuale c'è un piccolo refuso (manca la chiusura delle virgolette e c'è uno spazio extra)
        # Il test si aspetta il comportamento attuale del tuo metodo:
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty(self):
        """Verifica che restituisca una stringa vuota se non ci sono proprietà"""
        node = HTMLNode(tag="p", value="Hello")
        self.assertEqual(node.props_to_html(), "")

        node_none_props = HTMLNode(tag="p", props=None)
        self.assertEqual(node_none_props.props_to_html(), "")

    def test_values_assignment(self):
        """Verifica che gli attributi dell'oggetto siano assegnati correttamente nel costruttore"""
        node = HTMLNode(
            tag="div", value="Contenuto", children=["child1"], props={"class": "main"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Contenuto")
        self.assertEqual(node.children, ["child1"])
        self.assertEqual(node.props, {"class": "main"})

    def test_repr(self):
        """Verifica che la rappresentazione testuale dell'oggetto sia corretta"""
        node = HTMLNode(tag="h1", value="Titolo")
        expected_repr = "Tag: h1 Value: Titolo Children: None Props: None"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
