import unittest
from block_markdown import markdown_to_blocks

class TestBlockMarkdown(unittest.TestCase):
    def test_conversion_to_blocks(self):
        input = "This is **bolded** paragraph\n\
\n\
This is another paragraph with *italic* text and `code` here\n\
This is the same paragraph on a new line\n\
\n\
* This is a list\n\
* with items"
        blocks = 3
        self.assertEqual(blocks, len(markdown_to_blocks(input)))
