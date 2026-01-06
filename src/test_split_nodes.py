import unittest
from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        result = text_to_textnodes(text)
        self.assertListEqual(expect, result)

    def test_delim_basic_code(self):
        # Caso: Un blocco di codice al centro
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_delim_bold_multi(self):
        # Caso: Multipli blocchi (es. bold **)
        node = TextNode("This is *bold* and *more bold*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)

        self.assertEqual(len(new_nodes), 4)  # "This is ", "bold", " and ", "more bold"
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "more bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_delim_italic_start_end(self):
        # Caso: Delimitatore all'inizio e alla fine
        # "*italic* text" -> split crea ["", "italic", " text"]
        node = TextNode("_italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "italic")
        self.assertEqual(new_nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, " text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_delim_no_delimiters(self):
        # Caso: Nessun delimitatore presente
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_delim_error_unclosed(self):
        # Caso: Delimitatore non chiuso (errore di sintassi Markdown)
        # "text `code" -> split crea ["text ", "code"] -> lunghezza 2 (pari) -> Errore
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_node(self):
        # Caso: Passiamo nodi misti
        node_bg = TextNode("Already Bold", TextType.BOLD)
        node_txt = TextNode("Normal text", TextType.TEXT)

        # Supponiamo di cercare codice (`), ma abbiamo già del grassetto
        new_nodes = split_nodes_delimiter([node_bg, node_txt], "`", TextType.CODE)

        # ORA ci aspettiamo 2 nodi: il BOLD preservato + il TEXT processato
        self.assertEqual(len(new_nodes), 2)

        # Verifichiamo che il primo sia rimasto BOLD
        self.assertEqual(new_nodes[0].text, "Already Bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

        # Verifichiamo che il secondo sia rimasto TEXT (non c'erano backticks)
        self.assertEqual(new_nodes[1].text, "Normal text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        # Ci aspettiamo 2 nodi: "This is text with an " (TEXT) e l'immagine (IMAGE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_image_double(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        # Ci aspettiamo: Text -> Image -> Text -> Image
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text, "image")  # Image 1
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "second image")  # Image 2

    def test_split_image_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no images")

    # --- TEST PER I LINK ---

    def test_split_link_single(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) to boot dev",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        # Ci aspettiamo: Text -> Link -> Text
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[2].text, " to boot dev")

    def test_split_link_multi(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "another")

    def test_split_link_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)


if __name__ == "__main__":
    unittest.main()
