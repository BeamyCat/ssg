from enum import Enum
import re
from textnode import TextType, TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from util import text_to_textnodes, text_node_to_html_node


BlockType = Enum("BlockType", [
    "PARAGRAPH",
    "HEADING",
    "CODE",
    "QUOTE",
    "UNORDERED_LIST",
    "ORDERED_LIST",
])


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split('\n\n')
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != "", blocks))
    return blocks


def is_block_heading(block: str) -> bool:
    prefix = block.partition(' ')[0]
    if len(prefix) < 1 or 6 < len(prefix):
        return False
    for char in prefix:
        if char != '#':
            return False
    return True

def is_block_code(block: str) -> bool:
    return block.startswith('```') and block.endswith('```')

def is_block_quote(block: str) -> bool:
    lines = block.splitlines()
    for line in lines:
        if not line.startswith('> '):
            return False
    return len(lines) > 0

def is_block_unordered_list(block: str) -> bool:
    lines = block.splitlines()
    for line in lines:
        if not line.startswith('- '):
            return False
    return len(lines) > 0

def is_block_ordered_list(block: str) -> bool:
    lines = block.splitlines()
    for line in lines:
        if re.match(r"^\d+\. ", line) == None:
            return False
    return len(lines) > 0

def block_to_block_type(block: str) -> BlockType:
    if is_block_heading(block):
        return BlockType.HEADING
    if is_block_code(block):
        return BlockType.CODE
    if is_block_quote(block):
        return BlockType.QUOTE
    if is_block_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_block_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[LeafNode]:
    return list(map(text_node_to_html_node, text_to_textnodes(text)))

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    branch_nodes: list[ParentNode] = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                children: list[LeafNode] = text_to_children(block.replace('\n', ' '))
                branch_nodes.append(ParentNode('p', children))
                
            case BlockType.HEADING:
                tag: str = 'h' + str(block.partition(' ')[0].count('#'))
                children: list[LeafNode] = text_to_children(block.lstrip('# '))
                branch_nodes.append(ParentNode(tag, children))
                
            case BlockType.CODE:
                text: str = block.strip('`').strip()
                node: LeafNode = LeafNode('code', text)
                branch_nodes.append(ParentNode('pre', [node]))
            
            case BlockType.QUOTE:
                text: str = ' '.join(list(map(
                    lambda line: line.lstrip('> '), 
                    block.splitlines()
                )))
                children: list[LeafNode] = text_to_children(text)
                branch_nodes.append(ParentNode('blockquote', children))
                    
#                lines: list[str] = block.splitlines()
#                nodes: list[LeafNode] = []
#                for line in lines:
#                    nodes.extend(text_to_children(line.lstrip('> ')))
#                branch_nodes.append(ParentNode('blockquote', nodes))
            
            case BlockType.UNORDERED_LIST:
                items: list[str] = block.splitlines()
                nodes: list[ParentNode] = []
                for item in items:
                    nodes.append(ParentNode(
                        'li', text_to_children(item.lstrip('- '))))
                branch_nodes.append(ParentNode('ul', nodes))
            
            case BlockType.ORDERED_LIST:
                items: list[str] = block.splitlines()
                nodes: list[ParentNode] = []
                for item in items:
                    nodes.append(ParentNode(
                        'li', text_to_children(item.partition(' ')[2])))
                branch_nodes.append(ParentNode('ol', nodes))
    
    return ParentNode('div', branch_nodes)
        









