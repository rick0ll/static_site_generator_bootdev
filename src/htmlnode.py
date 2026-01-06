class HTMLNode:
    def __init__(
        self,
        tag=None,
        value=None,
        props: dict[str, str] | None = None,
        children=None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if not self.props or 0 == len(self.props):
            return result

        for key, value in self.props.items():
            result += key + '="' + value + '" '

        result = result[: len(result) - 1]
        return result

    def __repr__(self) -> str:
        return f"Tag: {self.tag} Value: {self.value} Children: {self.children} Props: {self.props}"
