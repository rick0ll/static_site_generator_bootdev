from block_type import block_to_block_type, BlockType
from conversion import text_node_to_html_node
from htmlnode import HTMLNode
import htmlnode
from markdown_to_blocks import markdown_to_blocks
from split_nodes import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import *
import re


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children.append(block_to_paragraph(block))
        elif block_type == BlockType.HEADING:
            children.append(block_to_heading(block))
        elif block_type == BlockType.CODE:
            children.append(block_to_code(block))
        elif block_type == BlockType.QUOTE:
            children.append(block_to_quote(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(block_to_ul(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(block_to_ol(block))
        else:
            raise ValueError("Invalid block type")

    return ParentNode("div", children, None)


def text_to_children(text, block_type=None):
    if block_type == BlockType.CODE:
        return [text_node_to_html_node(TextNode(text, TextType.TEXT))]

    children_textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(child) for child in children_textnodes]


def block_to_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def block_to_heading(block):
    # Contiamo i cancelletti
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    if level + 1 < len(block):
        text = block[level + 1 :]  # Rimuoviamo '# '
    else:
        text = block[level:]

    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def block_to_code(block):
    # Rimuoviamo ``` all'inizio e alla fine e i newline extra
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-4]  # Rimuove ```\n e ```

    # Il blocco code non deve parsare il markdown interno, quindi usiamo un LeafNode diretto
    code_node = LeafNode("code", text)
    return ParentNode("pre", [code_node])


def block_to_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        # Rimuoviamo '> ' da ogni riga
        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def block_to_ul(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]  # Rimuove "* " o "- "
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def block_to_ol(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        # Rimuove "1. " (trova il primo punto e spazio)
        text = item[item.find(". ") + 2 :]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
