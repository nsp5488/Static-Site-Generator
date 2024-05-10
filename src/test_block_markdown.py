import unittest
from block_markdown import *
from leafnode import LeafNode
class TestBlockMarkdown(unittest.TestCase):
    def test_conversion_to_blocks(self):
        input = "This is **bolded** paragraph\n\
\n\
This is another paragraph with *italic* text and `code` here\n\
This is the same paragraph on a new line\n\
\n\
* This is a list\n\
* with items"
        blocks = markdown_to_blocks(input)

        self.assertEqual(3, len(blocks))


    def test_conversion_to_blocks_all_types(self):
        b1 = '### abc\n\n'
        b2 = '```\ncode text\n```\n\n'
        b3 = '> line1 of quote\n>line2 of quote\n\n'
        b4 = '* unordered\n* list\n- continues\n\n'
        b5 = '1. ordered\n2. list\n\n'
        b6 = 'test paragraph\nline2\n\n'
        markdown = "".join([b1,b2,b3,b4,b5,b6])
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(6, len(blocks))

    def test_block_to_block_type(self):
        b1 = '### abc'
        b2 = '``` code\ntext ```'
        b3 = '> line1 of quote\n>line2 of quote'
        b4 = '* unordered\n* list\n- continues'
        b5 = '1. ordered\n2. list'
        b6 = 'paragraph'
        expected = [block_type_heading, block_type_code, block_type_quote,
                     block_type_unordered_list, block_type_ordered_list, block_type_paragraph]
        
        actual = list(map(block_to_block_type, [b1,b2,b3,b4,b5, b6]))

        self.assertListEqual(expected, actual)

    def test_markdown_to_html_heading(self):
        b1 = '### abc'
        expected = ParentNode("div", [ParentNode("h3", [LeafNode(None, "abc")])])
        actual = markdown_to_html_node(b1)

        # casting to string to avoid python checking equality via memory location
        self.assertEqual(str(expected), str(actual))

    def test_markdown_to_html_code(self):
        b1 = '``` code\ntext ```'
        expected = ParentNode("div", [ParentNode("pre", [ParentNode("code", \
        [LeafNode(None, ' code'), LeafNode(None, 'text ')])])] )

        actual = markdown_to_html_node(b1)
        self.assertEqual(str(expected), str(actual))


    def test_markdown_to_html_quote(self):
        b1 = '> line1 of quote\n>line2 of quote'
        expected = ParentNode("div", [ParentNode("blockquote",\
        [LeafNode(None, "line1 of quote"), LeafNode(None, "line2 of quote")])])
        actual = markdown_to_html_node(b1)

        self.assertEqual(str(expected), str(actual))

    def test_markdown_to_html_ul(self):
        b1 = '* unordered\n* list\n- continues'
        expected = ParentNode("div", [ParentNode("ul", [LeafNode("li", "unordered"), LeafNode("li", "list"), LeafNode("li", "continues")])])
        actual = markdown_to_html_node(b1)

        self.assertEqual(str(expected), str(actual))

    def test_markdown_to_html_ol(self):
        b = '1. ordered\n2. list'
        expected = ParentNode("div", [ParentNode("ol", [LeafNode("li", "ordered"), LeafNode("li", "list")])])
        actual = markdown_to_html_node(b)

        self.assertEqual(str(expected), str(actual))


    def test_markdown_to_html_paragraph(self):
        b = 'test paragraph line2'
        expected = ParentNode("div", [ParentNode("p", [LeafNode(None, 'test paragraph line2')])])
        actual = markdown_to_html_node(b)
        self.assertEqual(str(expected), str(actual))

    def test_full_markdown_to_html(self):
        b1 = '### abc\n\n'
        b2 = '```code text```\n\n'
        b3 = '> line1 of quote\n>line2 of quote\n\n'
        b4 = '* unordered\n* list\n- continues\n\n'
        b5 = '1. ordered\n2. list\n\n'
        b6 = 'test paragraph line2\n\n'
        markdown = "\n".join([b1,b2,b3,b4,b5,b6])
        expected = ParentNode("div", [
            ParentNode("h3", [LeafNode(None, "abc")]),
            ParentNode("pre", [ParentNode("code", [LeafNode(None, 'code text')])]),
            ParentNode("blockquote", [LeafNode(None, "line1 of quote"), LeafNode(None, "line2 of quote")]),
            ParentNode("ul", [LeafNode("li", "unordered"), LeafNode("li", "list"), LeafNode("li", "continues")]),
            ParentNode("ol", [LeafNode("li", "ordered"), LeafNode("li", "list")]),
            ParentNode("p", [LeafNode(None, 'test paragraph line2')])
        ])
        actual = markdown_to_html_node(markdown)
        self.assertEqual(str(expected), str(actual))