import unittest
from block_type import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_block_heading(self):
        # H1
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        # H6
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        # Casi che DOVREBBERO essere paragrafi:
        # 7 hash non sono un heading
        self.assertEqual(
            block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH
        )
        # Manca lo spazio
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_block_code(self):
        # Codice su una riga
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)

        # Codice multiriga (fondamentale per Markdown reale)
        code_block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

        # Backtick non chiusi o numero errato -> Paragrafo
        self.assertEqual(block_to_block_type("`` not code ``"), BlockType.PARAGRAPH)

    def test_block_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        # Quote multiriga
        quote = "> Line 1\n> Line 2"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_block_unordered_list(self):
        # Test con trattino
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)

        # Test che richiede lo spazio dopo il trattino
        self.assertEqual(block_to_block_type("-NoSpace"), BlockType.PARAGRAPH)

    def test_block_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(
            block_to_block_type("1. Long number list\n2. taac"), BlockType.ORDERED_LIST

        )

        # Manca il punto
        self.assertEqual(block_to_block_type("1 Item"), BlockType.PARAGRAPH)
        # Manca lo spazio
        self.assertEqual(block_to_block_type("1.NoSpace"), BlockType.PARAGRAPH)

    def test_block_paragraph(self):
        self.assertEqual(block_to_block_type("Just text"), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("This is a\nmultiline paragraph"), BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()
