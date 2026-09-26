from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a non-empty tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        html = ""
        for child in self.children:
            html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
