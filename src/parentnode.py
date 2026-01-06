from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: dict[str, str] | None = None) -> None:
        if tag == "":
            tag = None
        super().__init__(tag=tag, props=props, children=children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag on HTML Parent Node")
        if self.children is None:
            raise ValueError("Missing children on HTML Parent Node")

        children_html = [children.to_html() for children in self.children]
        props_html = "" if not self.props else " " + self.props_to_html()
        html = f'<{self.tag}{props_html}>{"".join(children_html)}</{self.tag}>'

        return html
