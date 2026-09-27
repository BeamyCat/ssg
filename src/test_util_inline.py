import unittest
from textnode import TextNode, TextType
from inline import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestUtilInline(unittest.TestCase):
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
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        test_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        test_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_italic(self):
        node = TextNode("This is text with an _italic phrase_ in the middle", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        test_nodes = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_multiple(self):
        node = TextNode("plain _italic_ plain _italic_ plain", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
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
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        test_nodes = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_ends_with(self):
        node = TextNode("plain _italic_ plain _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        test_nodes = [
            TextNode("plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_clamped_with(self):
        node = TextNode("_italic_ plain _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        test_nodes = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" plain ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_split_mismatched(self):
        node = TextNode("This text has _mismatched_ delimiters_", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], '_', TextType.ITALIC)
    
    def test_split_mismatched2(self):
        node = TextNode("This _text has _mismatched_ delimiters", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], '_', TextType.ITALIC)
    
    def test_split_no_delimiters(self):
        node = TextNode("This text has no delimiters", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
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
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
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
    
    ########## EXTRACT MARKDOWN IMAGES & LINKS ##########
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
    
    ########## SPLIT NODES IMAGES & LINKS ##########
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image",
                    TextType.IMAGE, 
                    "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", 
                    TextType.LINK, 
                    "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_not_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)],
            new_nodes,
        )
    
    def test_split_links_not_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)],
            new_nodes,
        )
    
    def test_split_multiple_images(self):
        node = TextNode(
            "Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) And here's Vivian :3 ![Vivian Cottonsmith](https://beamycat.neocities.org/art/img/vivian-cottonsmith.png)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("Here's Roxie! ", TextType.PLAIN),
            TextNode("Roxanne Rohls", TextType.IMAGE, "https://beamycat.neocities.org/art/img/roxie-rohls.png"),
            TextNode(" And here's Vivian :3 ", TextType.PLAIN),
            TextNode("Vivian Cottonsmith", TextType.IMAGE, "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png"),
        ], new_nodes)
    
    def test_split_multiple_nodes_images(self):
        node_1 = TextNode(
            "Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png)",
            TextType.PLAIN
        )
        node_2 = TextNode(
            " And here's Vivian :3 ![Vivian Cottonsmith](https://beamycat.neocities.org/art/img/vivian-cottonsmith.png)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node_1, node_2])
        self.assertListEqual([
            TextNode("Here's Roxie! ", TextType.PLAIN),
            TextNode("Roxanne Rohls", TextType.IMAGE, "https://beamycat.neocities.org/art/img/roxie-rohls.png"),
            TextNode(" And here's Vivian :3 ", TextType.PLAIN),
            TextNode("Vivian Cottonsmith", TextType.IMAGE, "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png"),
        ], new_nodes)
    
    def test_split_multiple_links(self):
        node = TextNode(
            "My website is [BeamyCat](https://beamycat.neocities.org). My friend Robin's site is [Robin Problem](https://robinproblem.neocities.org/).",
            TextType.PLAIN
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("My website is ", TextType.PLAIN),
            TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org"),
            TextNode(". My friend Robin's site is ", TextType.PLAIN),
            TextNode("Robin Problem", TextType.LINK, "https://robinproblem.neocities.org/"),
            TextNode(".", TextType.PLAIN),
        ], new_nodes)
    
    def test_split_multiple_nodes_links(self):
        node_1 = TextNode(
            "My website is [BeamyCat](https://beamycat.neocities.org)",
            TextType.PLAIN
        )
        node_2 = TextNode(
            ". My friend Robin's site is [Robin Problem](https://robinproblem.neocities.org/).",
            TextType.PLAIN
        )
        new_nodes = split_nodes_link([node_1, node_2])
        self.assertListEqual([
            TextNode("My website is ", TextType.PLAIN),
            TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org"),
            TextNode(". My friend Robin's site is ", TextType.PLAIN),
            TextNode("Robin Problem", TextType.LINK, "https://robinproblem.neocities.org/"),
            TextNode(".", TextType.PLAIN),
        ], new_nodes)
    
    def test_split_images_with_link(self):
        node = TextNode(
            "My website is [BeamyCat](https://beamycat.neocities.org). Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) And here's Vivian :3 ![Vivian Cottonsmith](https://beamycat.neocities.org/art/img/vivian-cottonsmith.png)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("My website is [BeamyCat](https://beamycat.neocities.org). Here's Roxie! ", TextType.PLAIN),
            TextNode("Roxanne Rohls", TextType.IMAGE, "https://beamycat.neocities.org/art/img/roxie-rohls.png"),
            TextNode(" And here's Vivian :3 ", TextType.PLAIN),
            TextNode("Vivian Cottonsmith", TextType.IMAGE, "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png"),
        ], new_nodes)
    
    def test_split_links_with_image(self):
        node = TextNode(
            "Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) My website is [BeamyCat](https://beamycat.neocities.org). My friend Robin's site is [Robin Problem](https://robinproblem.neocities.org/).",
            TextType.PLAIN
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) My website is ", TextType.PLAIN),
            TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org"),
            TextNode(". My friend Robin's site is ", TextType.PLAIN),
            TextNode("Robin Problem", TextType.LINK, "https://robinproblem.neocities.org/"),
            TextNode(".", TextType.PLAIN),
        ], new_nodes)
    
    def test_split_images_and_links(self):
        self.maxDiff = None
        node = TextNode(
            "My website is [BeamyCat](https://beamycat.neocities.org). My friend Robin's site is [Robin Problem](https://robinproblem.neocities.org/). Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) And here's Vivian :3 ![Vivian Cottonsmith](https://beamycat.neocities.org/art/img/vivian-cottonsmith.png)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual([
            TextNode("My website is ", TextType.PLAIN),
            TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org"),
            TextNode(". My friend Robin's site is ", TextType.PLAIN),
            TextNode("Robin Problem", TextType.LINK, "https://robinproblem.neocities.org/"),
            TextNode(". Here's Roxie! ", TextType.PLAIN),
            TextNode("Roxanne Rohls", TextType.IMAGE, "https://beamycat.neocities.org/art/img/roxie-rohls.png"),
            TextNode(" And here's Vivian :3 ", TextType.PLAIN),
            TextNode("Vivian Cottonsmith", TextType.IMAGE, "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png"),
        ], new_nodes)
    
    def test_split_links_then_images(self):
        self.maxDiff = None
        node = TextNode(
            "My website is [BeamyCat](https://beamycat.neocities.org). My friend Robin's site is [Robin Problem](https://robinproblem.neocities.org/). Here's Roxie! ![Roxanne Rohls](https://beamycat.neocities.org/art/img/roxie-rohls.png) And here's Vivian :3 ![Vivian Cottonsmith](https://beamycat.neocities.org/art/img/vivian-cottonsmith.png)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image(split_nodes_link([node]))
        self.assertListEqual([
            TextNode("My website is ", TextType.PLAIN),
            TextNode("BeamyCat", TextType.LINK, "https://beamycat.neocities.org"),
            TextNode(". My friend Robin's site is ", TextType.PLAIN),
            TextNode("Robin Problem", TextType.LINK, "https://robinproblem.neocities.org/"),
            TextNode(". Here's Roxie! ", TextType.PLAIN),
            TextNode("Roxanne Rohls", TextType.IMAGE, "https://beamycat.neocities.org/art/img/roxie-rohls.png"),
            TextNode(" And here's Vivian :3 ", TextType.PLAIN),
            TextNode("Vivian Cottonsmith", TextType.IMAGE, "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png"),
        ], new_nodes)
    
    ########## TEXT TO TEXTNODES ##########
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        test_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, test_nodes)
    
    def test_text_to_textnodes2(self):
        text = "This is text with a [link to BeamyCat](https://beamycat.neocities.org), an image of BeamyCat ![Picrew](https://beamycat.neocities.org/img/picrew/beamy_picrew.png), and some `awesome code`. _Per aspera ad astra_. **\"Become endless? To hell with that! I'm happy right here, right now.\"**"
        nodes = text_to_textnodes(text)
        test_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("link to BeamyCat", TextType.LINK, "https://beamycat.neocities.org"),
            TextNode(", an image of BeamyCat ", TextType.PLAIN),
            TextNode("Picrew", TextType.IMAGE, "https://beamycat.neocities.org/img/picrew/beamy_picrew.png"),
            TextNode(", and some ", TextType.PLAIN),
            TextNode("awesome code", TextType.CODE),
            TextNode(". ", TextType.PLAIN),
            TextNode("Per aspera ad astra", TextType.ITALIC),
            TextNode(". ", TextType.PLAIN),
            TextNode("\"Become endless? To hell with that! I'm happy right here, right now.\"", TextType.BOLD),
        ]
        self.assertListEqual(nodes, test_nodes)
    
        


if __name__ == "__main__":
    unittest.main()

