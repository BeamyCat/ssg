from textnode import TextNode, TextType
from leafnode import LeafNode
import re


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {
                "src": text_node.url,
                "alt": text_node.text,
            })
    raise ValueError("text_node has invalid TextType")


def split_node_delimiter(text_node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    if text_node.text.count(delimiter) % 2 != 0:
        raise Exception("missing matching delimiter")
    
    in_tags: bool = text_node.text.startswith(delimiter)
    text: str = text_node.text.strip(delimiter)
    split_texts: list[str] = text.split(delimiter)
    new_nodes: list[TextNode] = []
    
    for current in split_texts:
        new_nodes.append(TextNode(current, text_type if in_tags else text_node.text_type))
        in_tags = not in_tags
    
    return new_nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        new_nodes.extend(split_node_delimiter(node, delimiter, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)









