import unittest

from textnode import TextNode, split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("test node", "test")
        node2 = TextNode("test node", "")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("a", "b", 'test.com')
        self.assertEqual("TextNode(a, b, test.com)", str(node1))

    @unittest.expectedFailure
    def test_invalid_constructor(self):
        _ = TextNode("a")

    def test_split_nodes_code(self):
        text_type_text = "text"
        text_type_bold = "bold"
        text_type_code = "code"
        text_type_italics = "italic"
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        expected = [
                        TextNode("This is text with a ", text_type_text),
                        TextNode("code block", text_type_code),
                        TextNode(" word", text_type_text),
                    ]
        for e, a in zip(expected, new_nodes):
            self.assertEqual(e, a)


    def test_split_nodes_bold(self):
        text_type_text = "text"
        text_type_bold = "bold"
        text_type_code = "code"
        text_type_italics = "italic"

        node = TextNode("This is text with a **bold** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_bold)

        expected = [
                        TextNode("This is text with a ", text_type_text),
                        TextNode("bold", text_type_bold),
                        TextNode(" word", text_type_text),
                    ]
        for e, a in zip(expected, new_nodes):
            self.assertEqual(e, a)


    def test_split_nodes_italic(self):
        text_type_text = "text"
        text_type_bold = "bold"
        text_type_code = "code"
        text_type_italics = "italic"

        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italics)

        expected = [
                        TextNode("This is text with an ", text_type_text),
                        TextNode("italic", text_type_italics),
                        TextNode(" word", text_type_text),
                    ]
        for e, a in zip(expected, new_nodes):
            self.assertEqual(e, a)

    def test_invalid_markdown_fails(self):
        node = TextNode("this is **invalid markdown!", 'text')
        self.assertRaises(Exception, split_nodes_delimiter,[[node], '**', 'bold'])


    def test_split_images(self):
        text_type_text = "text"
        text_type_image = 'image'
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])

        expected = [
                        TextNode("This is text with an ", text_type_text),
                        TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                        TextNode(" and another ", text_type_text),
                        TextNode(
                            "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                        ),
                    ]
        for e, a in zip(expected, new_nodes):
            self.assertEqual(e, a)
            
    def test_split_markdown(self):
        text_type_text = "text"
        text_type_link = 'link'
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node]) 

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_link, "https://www.example.com/another")
        ]

        for e, a in zip(expected, new_nodes):
            self.assertEqual(e, a)

            
if __name__ == "__main__":
    unittest.main()
