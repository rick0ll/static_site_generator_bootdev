from enum import Enum


class TextType(Enum):
    TEXT = "plain text"
    BOLD = "**bold text**"
    ITALIC = "_italic text_"
    CODE = "`code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = ""):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        return (
            obj.text == self.text
            and obj.text_type == self.text_type
            and obj.url == self.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
