from textnode import TextNode, TextType

def main() -> None:
    text_node = TextNode("Per aspera ad astra.", TextType.LINK, "https://beamycat.neocities.org")
    print(text_node)

main()
