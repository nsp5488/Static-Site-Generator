from leafnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_code = "code"
text_type_italics = "italic"
text_type_image = 'image'
text_type_link = "link"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url 
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text, None)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text, None)
    if text_node.text_type == text_type_italics:
        return LeafNode("i", text_node.text, None)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text, None)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {'href': text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode('img', text_node.text, {'src':text_node.url, 'alt':text_node.text})

    raise Exception("Invalid text type for conversion")