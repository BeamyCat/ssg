import unittest
from blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestUtilBlock(unittest.TestCase):
    ########## MARKDOWN TO BLOCKS ##########
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_extra_ws(self):
        md = """

May you attain enlightenment:

1. Diagonal Fire
2. Rearcannon
3. Tiny Valor


Per aspera ad astra.



The adventure of life goes on!

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual([
            "May you attain enlightenment:",
            "1. Diagonal Fire\n2. Rearcannon\n3. Tiny Valor",
            "Per aspera ad astra.",
            "The adventure of life goes on!",
        ], blocks)
    
    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual([], blocks)
    
    def test_markdown_to_blocks_just_ws(self):
        md = "\n    \n\n        \n\n\n          \n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual([], blocks)
    
    ########## BLOCK TO BLOCK TYPE ##########
    def test_block_to_type_paragraph(self):
        block = "Per aspera ad astra."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_type_paragraph2(self):
        block = """Per aspera ad astra.
Ad meliora.
The adventure of life goes on!"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_type_paragraph_empty(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_type_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_type_h2(self):
        block = "## This, too, is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_type_h6(self):
        block = "###### This is the smallest heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_type_not_h7(self):
        block = "####### This has too many #'s to be a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_type_malformed_heading(self):
        block = "#This is not a valid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_type_code(self):
        block = """```
DIS-OS ERROR REPORT
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_to_type_quote(self):
        block = """> Become endless?
> To hell with that!
> I'm happy right here, right now."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_to_type_unordered_list(self):
        block = """- Per aspera ad astra.
- Ad meliora.
- The adventure of life goes on!"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_type_ordered_list(self):
        block = """1. Diagonal Fire
2. Rearcannon
3. Tiny Valor"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_type_ordered_list2(self):
        block = """1. Diagonal Fire
11. Rearcannon
111. Tiny Valor"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()

