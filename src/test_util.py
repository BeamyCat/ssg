import unittest
from textnode import TextNode, TextType
from util import text_node_to_html_node, split_node_delimiter, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestUtil(unittest.TestCase):
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
    
    ########## SPLIT NODE DELIMITER ##########
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '`', TextType.CODE)
        test_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '**', TextType.BOLD)
        test_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_italic(self):
        node = TextNode("This is text with an _italic phrase_ in the middle", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '_', TextType.ITALIC)
        test_nodes = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_multiple(self):
        node = TextNode("plain _italic_ plain _italic_ plain", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '_', TextType.ITALIC)
        test_nodes = [
            TextNode("plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_starts_with(self):
        node = TextNode("_italic_ plain _italic_ plain", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '_', TextType.ITALIC)
        test_nodes = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_ends_with(self):
        node = TextNode("plain _italic_ plain _italic_", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '_', TextType.ITALIC)
        test_nodes = [
            TextNode("plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_clamped_with(self):
        node = TextNode("_italic_ plain _italic_", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '_', TextType.ITALIC)
        test_nodes = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_mismatched(self):
        node = TextNode("This text has _mismatched_ delimiters_", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_node_delimiter(node, '_', TextType.ITALIC)
    
    def test_split_mismatched2(self):
        node = TextNode("This _text has _mismatched_ delimiters", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_node_delimiter(node, '_', TextType.ITALIC)
    
    def test_split_no_delimiters(self):
        node = TextNode("This text has no delimiters", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '_', TextType.ITALIC)
        test_nodes = [
            TextNode("This text has no delimiters", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("Become _endless_?", TextType.PLAIN),
            TextNode("To _hell_ with that!", TextType.PLAIN),
            TextNode("I'm happy right _here_, right _now_.", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
        test_nodes = [
            TextNode("Become ", TextType.PLAIN),
            TextNode("endless", TextType.ITALIC),
            TextNode("?", TextType.PLAIN),
            TextNode("To ", TextType.PLAIN),
            TextNode("hell", TextType.ITALIC),
            TextNode("with that!", TextType.PLAIN),
            TextNode("I'm happy right ", TextType.PLAIN),
            TextNode("here", TextType.ITALIC),
            TextNode(", right ", TextType.PLAIN),
            TextNode("now", TextType.ITALIC),
            TextNode(".", TextType.PLAIN),
        ]
    
    def test_split_multiple_types(self):
        node = TextNode("This text has **bolded words**, _italic words_, and `code words`.", TextType.PLAIN)
        new_nodes = split_node_delimiter(node, '**', TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
        test_nodes = [
            TextNode("This text has ", TextType.PLAIN),
            TextNode("bolded words", TextType.BOLD),
            TextNode(", ", TextType.PLAIN),
            TextNode("italic words", TextType.ITALIC),
            TextNode(", and ", TextType.PLAIN),
            TextNode("code words", TextType.CODE),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    ########## EXTRACT MARKDOWN IMAGES ##########
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://beamycat.neocities.org)"
        )
        self.assertListEqual([("link", "https://beamycat.neocities.org")], matches)
    
    def test_images_not_links(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://beamycat.neocities.org)"
        )
        self.assertListEqual([], matches)
    
    def test_links_not_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    
    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) And here's Vivian :3 ![Vivian Cottonsmith](https://beamycat.neocities.org/art/img/vivian-cottonsmith.png)"
        )
        self.assertListEqual([
            ("Roxanne Rohls", 
            "https://beamycat.neocities.org/art/img/roxie-rohls.png"),
            ("Vivian Cottonsmith", 
            "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png"),
        ], matches)
    
    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "My website is [BeamyCat](https://beamycat.neocities.org). My friend Robin's site is [Robin Problem](https://robinproblem.neocities.org/)."
        )
        self.assertListEqual([
            ("BeamyCat",
            "https://beamycat.neocities.org"),
            ("Robin Problem",
            "https://robinproblem.neocities.org/"),
        ], matches)
    
    def test_extract_images_with_link(self):
        matches = extract_markdown_images(
            "My website is [BeamyCat](https://beamycat.neocities.org). Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) And here's Vivian :3 ![Vivian Cottonsmith](https://beamycat.neocities.org/art/img/vivian-cottonsmith.png)"
        )
        self.assertListEqual([
            ("Roxanne Rohls", 
            "https://beamycat.neocities.org/art/img/roxie-rohls.png"),
            ("Vivian Cottonsmith", 
            "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png"),
        ], matches)
    
    def test_extract_links_with_image(self):
        matches = extract_markdown_links(
            "Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) My website is [BeamyCat](https://beamycat.neocities.org). My friend Robin's site is [Robin Problem](https://robinproblem.neocities.org/)."
        )
        self.assertListEqual([
            ("BeamyCat",
            "https://beamycat.neocities.org"),
            ("Robin Problem",
            "https://robinproblem.neocities.org/"),
        ], matches)
        

if __name__ == "__main__":
    unittest.main()

