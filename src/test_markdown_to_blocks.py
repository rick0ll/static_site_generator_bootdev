import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Caso base: due paragrafi separati da una riga vuota
        md = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "This is **bolded** paragraph")
        self.assertEqual(
            blocks[1],
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        )

    def test_markdown_to_blocks_newlines(self):
        # Caso complesso: troppi "a capo" e spazi vuoti extra
        md = """
            This is **bolded** paragraph




            This is another paragraph with *italic* text and `code` here
            """
        blocks = markdown_to_blocks(md)
        # Il tuo codice attuale fallirebbe qui (restituirebbe nodi vuoti nel mezzo)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(
            blocks[1], "This is another paragraph with *italic* text and `code` here"
        )

    def test_markdown_to_blocks_empty(self):
        # Caso limite: stringa vuota
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 0)
