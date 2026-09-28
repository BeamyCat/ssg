import unittest
from blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title


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
    
    ########## MARKDOWN TO HTML NODE ##########
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_markdown_to_html_node(self):
        self.maxDiff = None
        md = """
# This is a heading

## This is a smaller heading

###### This is the smallest heading

This is text with a [link to BeamyCat](https://beamycat.neocities.org), an image of BeamyCat ![Picrew](https://beamycat.neocities.org/img/picrew/beamy_picrew.png), and some `awesome code`. _Per aspera ad astra_. **\"Become endless? To hell with that! I'm happy right here, right now.\"**

```
DIS-OS REPORT 01/09/102023
FATAL_ERROR: *BR NULL*
```

> Become endless?c
> **To hell with that!**
> I'm happy right _here_, right _now_.
> Because I love you.

- Per aspera ad astra.
- _Ad meliora._
- **The adventure of life goes on!**

## **MAY YOU ATTAIN ENLIGHTENMENT**

1. DIAGONAL FIRE
2. **REARCANNON**
11. _TINY VALOR_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><h1>This is a heading</h1><h2>This is a smaller heading</h2><h6>This is the smallest heading</h6><p>This is text with a <a href="https://beamycat.neocities.org">link to BeamyCat</a>, an image of BeamyCat <img src="https://beamycat.neocities.org/img/picrew/beamy_picrew.png" alt="Picrew"></img>, and some <code>awesome code</code>. <i>Per aspera ad astra</i>. <b>"Become endless? To hell with that! I\'m happy right here, right now."</b></p><pre><code>DIS-OS REPORT 01/09/102023\nFATAL_ERROR: *BR NULL*</code></pre><blockquote>Become endless? <b>To hell with that!</b> I\'m happy right <i>here</i>, right <i>now</i>. Because I love you.</blockquote><ul><li>Per aspera ad astra.</li><li><i>Ad meliora.</i></li><li><b>The adventure of life goes on!</b></li></ul><h2><b>MAY YOU ATTAIN ENLIGHTENMENT</b></h2><ol><li>DIAGONAL FIRE</li><li><b>REARCANNON</b></li><li><i>TINY VALOR</i></li></ol></div>')


if __name__ == "__main__":
    unittest.main()

