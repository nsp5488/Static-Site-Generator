import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        ln = LeafNode("p", "This is a paragraph of text.")
        ln2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual("<p>This is a paragraph of text.</p>", ln.to_html())
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', ln2.to_html())

    def test_invalid_to_html(self):
        ln = LeafNode(None, None, None)
        self.assertRaises(ValueError, ln.to_html)

    def test_only_value_to_html(self):
        ln = LeafNode(None, "test", None)
        self.assertEqual("test", ln.to_html()) 
