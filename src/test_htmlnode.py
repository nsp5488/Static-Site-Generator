from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        h = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', h.props_to_html())

    def test_props_to_html_nonetype(self):
        h = HTMLNode(None, None, None, None)
        self.assertEquals('', h.props_to_html())


    def test_repr(self):
        ex = HTMLNode('a', 'test value', [HTMLNode(None, None, None, None)], 
                      {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("HTMLNode(a, test value, [HTMLNode(None, None, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})",
                         str(ex))
        
    