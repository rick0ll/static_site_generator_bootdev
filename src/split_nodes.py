import re
from textnode import TextNode, TextType
from get_markdown_anchors import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.extend(split_single_node_delimiter(old_node, text_type, delimiter))

    return new_nodes


def split_single_node_delimiter(old_node, text_type, delimiter):
    if old_node.text_type != TextType.TEXT:
        return [old_node]

    sections = old_node.text.split(delimiter)
    if len(sections) == 1:
        return [old_node]

    if len(sections) % 2 == 0:
        raise SyntaxError("Markdown badly formatted")

    current_nodes = []
    for i, value in enumerate(sections):
        if value == "":
            continue
        if i % 2 == 0:
            current_nodes.append(TextNode(text=value, text_type=TextType.TEXT))
        else:
            current_nodes.append(TextNode(text=value, text_type=text_type))
    return current_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.extend(split_single_node_img(old_node))
    return new_nodes


def split_single_node_img(old_node: TextNode):
    result = []
    if old_node.text_type != TextType.TEXT:
        return [old_node]

    img_values = extract_markdown_images(old_node.text)
    if len(img_values) == 0:
        return [old_node]

    texts = re.split(r"\!\[.*?\]\(.*?\)", old_node.text)

    for element in texts:
        if element == "":
            continue
        result.append(TextNode(element, TextType.TEXT))

        if len(img_values) != 0:
            img_value = img_values.pop(0)
            result.append(TextNode(img_value[0], TextType.IMAGE, img_value[1]))

    return result


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.extend(split_single_node_link(old_node))
    return new_nodes


def split_single_node_link(old_node: TextNode):
    result = []
    if old_node.text_type != TextType.TEXT:
        return [old_node]

    img_values = extract_markdown_links(old_node.text)
    if len(img_values) == 0:
        return [old_node]

    texts = re.split(r"(?<!!)\[.*?\]\(.*?\)", old_node.text)

    for element in texts:
        if element != "":
            result.append(TextNode(element, TextType.TEXT))

        if len(img_values) != 0:
            img_value = img_values.pop(0)
            result.append(TextNode(img_value[0], TextType.LINK, img_value[1]))

    return result


def text_to_textnodes(text):
    textnode_text = [TextNode(text, TextType.TEXT)]

    result = split_nodes_link(textnode_text)
    result = split_nodes_image(result)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "`", TextType.CODE)

    return result
