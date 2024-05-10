from leafnode import LeafNode
import re

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url 
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text, None)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text, None)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text, None)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text, None)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {'href': text_node.url})
    if text_node.text_type == "image":
        return LeafNode('img', None, {'src':text_node.url, 'alt':text_node.text})

    raise Exception("Invalid text type for conversion")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    text_type_text = "text"

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        line = node.text
        if delimiter in line:
            sections = line.split(delimiter)
            if len(sections) < 3:
                raise Exception("Invalid markdown! {line} has mismatched delimiters of type {delimiter}.")
            new_nodes.extend([
                TextNode(sections[0], text_type_text),
                TextNode(sections[1], text_type),
                TextNode(sections[2], text_type_text)
            ])
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    text_type_text = 'text'
    text_type_image = 'image'
    for node in old_nodes:
        split_line = extract_markdown_images(node.text)
        line = node.text
        if len(split_line) == 0:
            new_nodes.append(node)
            continue
        
        for alt, url in split_line:
            sections = line.split(f"![{alt}]({url})", 1)
            new_nodes.extend([
                TextNode(sections[0], text_type_text),
                TextNode(alt, text_type_image, url)
            ])
            if len(sections) > 1:
                line = sections[1]
        if len(line) > 0:
            new_nodes.append(TextNode(line, text_type_text))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    text_type_text = 'text'
    text_type_link = 'link'
    for node in old_nodes:
        split_line = extract_markdown_links(node.text)
        line = node.text
        if len(split_line) == 0:
            new_nodes.append(node)
            continue
        
        for text, url in split_line:
            sections = line.split(f"[{text}]({url})", 1)
            new_nodes.extend([
                TextNode(sections[0], text_type_text),
                TextNode(text, text_type_link, url)
            ])
            if len(sections) > 1:
                line = sections[1]
        if len(line) > 0:
            new_nodes.append(TextNode(line, text_type_text))

    return new_nodes