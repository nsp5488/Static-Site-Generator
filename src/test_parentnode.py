import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])

        html = node.to_html()

        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
                         html)

    def test_nested_parents(self):
        node = ParentNode(
            "h1", [
                ParentNode("b", [LeafNode('p', 'inner text')])
            ]
        )
        self.assertEqual("<h1><b><p>inner text</p></b></h1>", node.to_html())

    def test_with_props(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        {"href": "https://www.google.com", "target": "_blank"}
        )

        html = node.to_html()

        self.assertEqual('<p href="https://www.google.com" \
target="_blank"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>', html)


    def test_children_with_props(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text", {"href": "https://www.google.com", "target": "_blank"}),
            LeafNode(None, "Normal text"),
        ],
        )
        
        self.assertEqual('<p><b>Bold text</b>Normal text<i href="https://www.google.com" \
target="_blank">italic text</i>Normal text</p>',
                    node.to_html())
        
    def test_exceptions(self):
        invalid_node1 = ParentNode(None, None, None)
        invalid_node2 = ParentNode("a", None, None)

        self.failUnlessRaises(ValueError, invalid_node1.to_html)
        self.failUnlessRaises(ValueError, invalid_node2.to_html)
