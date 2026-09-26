import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_styles(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_to_html_many_children(self):
        child_1 = LeafNode("span", "child 1")
        child_2 = LeafNode("span", "child 2")
        child_3 = LeafNode("span", "child 3")
        parent_node = ParentNode("div", [child_1, child_2, child_3])
        self.assertEqual(parent_node.to_html(), "<div><span>child 1</span><span>child 2</span><span>child 3</span></div>")
    
    def test_to_html_with_props(self):
        child_node = LeafNode("a", "BeamyCat", {"href": "https://beamycat.neocities.org"})
        parent_node = ParentNode("div", [child_node], {"class": "banner"})
        self.assertEqual(parent_node.to_html(), '<div class="banner"><a href="https://beamycat.neocities.org">BeamyCat</a></div>')
    
    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_empty_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_no_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_empty_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
