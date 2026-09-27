from enum import Enum
import re


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
#    print(f"@@@{block}@@@")
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










