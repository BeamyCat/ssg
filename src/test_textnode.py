import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    ########## EQUALS ##########
    def test_eq(self):
        node = TextNode("foobar", TextType.PLAIN)
        node2 = TextNode("foobar", TextType.PLAIN)
        self.assertEqual(node, node2)
    
    def test_eq_italic(self):
        node = TextNode("Per aspera ad astra.", TextType.ITALIC)
        node2 = TextNode("Per aspera ad astra.", TextType.ITALIC)
        self.assertEqual(node, node2)
    
    def test_eq_bold(self):
        node = TextNode("Become endless? To hell with that!", TextType.BOLD)
        node2 = TextNode("Become endless? To hell with that!", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_code(self):
        node = TextNode("DIS-OS ERROR REPORT", TextType.CODE)
        node2 = TextNode("DIS-OS ERROR REPORT", TextType.CODE)
        self.assertEqual(node, node2)
    
    def test_eq_link(self):
        node = TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org")
        node2 = TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org")
        self.assertEqual(node, node2)
    
    def test_eq_image(self):
        node = TextNode("Picrew", TextType.IMAGE, "https://beamycat.neocities.org/img/picrew/beamy_picrew.png")
        node2 = TextNode("Picrew", TextType.IMAGE, "https://beamycat.neocities.org/img/picrew/beamy_picrew.png")
        self.assertEqual(node, node2)
    
    def test_eq_none(self):
        node = TextNode("Null link", TextType.LINK)
        node2 = TextNode("Null link", TextType.LINK, None)
        self.assertEqual(node, node2)
    
    ########## NOT EQUALS ##########
    def test_not_eq_text(self):
        node = TextNode("foobar", TextType.PLAIN)
        node2 = TextNode("foobaz", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_type(self):
        node = TextNode("foobar", TextType.PLAIN)
        node2 = TextNode("foobar", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_type_2(self):
        node = TextNode("Picrew", TextType.LINK, "https://beamycat.neocities.org/img/picrew/beamy_picrew.png")
        node2 = TextNode("Picrew", TextType.IMAGE, "https://beamycat.neocities.org/img/picrew/beamy_picrew.png")
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("foobar", TextType.LINK, "https://beamycat.neocities.org")
        node2 = TextNode("foobar", TextType.LINK, "https://beamycat.itch.io")
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url_2(self):
        node = TextNode("foobar", TextType.LINK, "https://beamycat.neocities.org")
        node2 = TextNode("foobar", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    ########## TEXT NODE TO HTML NODE ##########
    def test_text_node_to_html_node(self):
        node = TextNode("foobar", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "foobar")
    
    def test_to_html_italic(self):
        node = TextNode("Per aspera ad astra.", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "Per aspera ad astra.")
    
    def test_to_html_bold(self):
        node = TextNode("Become endless? To hell with that!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "Become endless? To hell with that!")
    
    def test_to_html_code(self):
        node = TextNode("DIS-OS ERROR REPORT", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "DIS-OS ERROR REPORT")
    
    def test_to_html_link(self):
        node = TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "BeamyCat")
        self.assertEqual(html_node.props, {"href": "https://beamycat.neocities.org"})
    
    def test_to_html_image(self):
        node = TextNode("Picrew", TextType.IMAGE, "https://beamycat.neocities.org/img/picrew/beamy_picrew.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://beamycat.neocities.org/img/picrew/beamy_picrew.png",
            "alt": "Picrew",
        })


if __name__ == "__main__":
    unittest.main()

