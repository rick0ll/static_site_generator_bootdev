from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag=None, value: str | None = None, props: dict[str, str] | None = None
    ) -> None:
        if tag == "":
            tag = None
        super().__init__(tag, value, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leafs node must have a value")

        if self.tag is None:
            return self.value

        props_html = "" if not self.props else " " + self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
