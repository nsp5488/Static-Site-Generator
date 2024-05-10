import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_bold,
    text_type_italics,
    text_type_image,
    text_type_link
)

from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_code(self):
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

    def integration_test(self):
        string = 'This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)'
        actual = text_to_textnodes(string)
        expected = [
                    TextNode("This is ", text_type_text),
                    TextNode("text", text_type_bold),
                    TextNode(" with an ", text_type_text),
                    TextNode("italic", text_type_italics),
                    TextNode(" word and a ", text_type_text),
                    TextNode("code block", text_type_code),
                    TextNode(" and an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", text_type_text),
                    TextNode("link", text_type_link, "https://boot.dev"),
                    ]
        self.assertListEqual(actual, expected)