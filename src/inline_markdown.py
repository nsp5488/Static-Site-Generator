import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_bold,
    text_type_italics,
    text_type_image,
    text_type_link
)

def text_to_textnodes(text):
    delimiters = ['`', '*', '**']
    text_types = [text_type_code, text_type_italics, text_type_bold]
    nodes = [TextNode(text, text_type_text, None)]

    for delimiter, type in zip(delimiters, text_types):
        nodes = split_nodes_delimiter(nodes, delimiter, type)

    return split_nodes_image(split_nodes_link(nodes))

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

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
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
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