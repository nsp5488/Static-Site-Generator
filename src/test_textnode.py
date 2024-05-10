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


if __name__ == "__main__":
    unittest.main()
