import unittest
from util import markdown_to_blocks


class TestUtilBlock(unittest.TestCase):
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










