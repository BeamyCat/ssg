import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("a", "Google", props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), html)
    
    def test_props2(self):
        node = HTMLNode("a", "BeamyCat", props={
            "href": "https://beamycat.neocities.org",
            "target": "_blank",
            "title": "BeamyCat | Gamedev + more!",
        })
        html = ' href="https://beamycat.neocities.org" target="_blank" title="BeamyCat | Gamedev + more!"'
        self.assertEqual(node.props_to_html(), html)
    
    def test_no_props(self):
        node = HTMLNode("p", "Google")
        html = ''
        self.assertEqual(node.props_to_html(), html)
    
    def test_empty_props(self):
        node = HTMLNode("p", "Google", props={})
        html = ''
        self.assertEqual(node.props_to_html(), html)


if __name__ == "__main__":
    unittest.main()

