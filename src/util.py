from textnode import TextNode, TextType
from leafnode import LeafNode
import re

#######################################
# INLINE FUNCTIONS
#######################################

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


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.IMAGE or node.text_type == TextType.LINK:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("missing matching delimiter")
        
        in_tags: bool = node.text.startswith(delimiter)
        text: str = node.text.strip(delimiter)
        split_texts: list[str] = text.split(delimiter)
        
        for current in split_texts:
            new_nodes.append(TextNode(
                current, 
                text_type if in_tags else node.text_type
            ))
            in_tags = not in_tags
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.IMAGE or node.text_type == TextType.LINK:
            new_nodes.append(node)
            continue
        text: str = node.text
        images: list[tuple[str, str]] = extract_markdown_images(text)
        for image in images:
            alt_text = image[0]
            url = image[1]
            sections = text.partition(f"![{alt_text}]({url})")
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], node.text_type))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = sections[2]
        if text != '':
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.IMAGE or node.text_type == TextType.LINK:
            new_nodes.append(node)
            continue
        text: str = node.text
        links: list[tuple[str, str]] = extract_markdown_links(text)
        for link in links:
            alt_text = link[0]
            url = link[1]
            sections = text.partition(f"[{alt_text}]({url})")
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], node.text_type))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            text = sections[2]
        if text != '':
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    return nodes


#######################################
# BLOCK FUNCTIONS
#######################################

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split('\n\n')
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != "", blocks))
    return blocks

        









