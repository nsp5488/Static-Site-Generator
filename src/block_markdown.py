import re
from parentnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = 'paragraph'
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    out = []
    block = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
           block.append(line)
        else:
            if len(block) > 0:
                out.append("\n".join(block))
                block = []
    if len(block) > 0:
        out.append("\n".join(block))
    return out

def find_starting_hashes(block):
    return re.findall(r"^#{1,6} ", block)

def block_to_block_type(block):
    if block.startswith("#"):
        match = find_starting_hashes(block)
        if match is not None:
            return block_type_heading
    if block.startswith('```') and block.endswith('```'):
        return block_type_code
    
    lines = block.split('\n')
    c = 1
    if len(lines) < 1:
        raise("Invalid markdown! No lines to parse.")
    can_be_quote = lines[0].startswith('>')
    can_be_ul = lines[0].startswith('- ') or lines[0].startswith('* ')
    can_be_ol = lines[0].startswith('1. ')

    if not (can_be_ol or can_be_quote or can_be_ul):
        return block_type_paragraph
    
    for line in lines:
        if can_be_quote and line.startswith('>'):
            can_be_ul = False
            can_be_ol = False

        if can_be_ul and line.startswith("* ") or line.startswith("- "):
            can_be_quote = False
            can_be_ol = False
            
        if can_be_ol and line.startswith(f"{c}. "):
            c += 1
            can_be_quote = False
            can_be_ul = False

    if can_be_quote:
        return block_type_quote
    if can_be_ul:
        return block_type_unordered_list
    if can_be_ol:
        return block_type_ordered_list
    
    return block_type_paragraph

def quote_to_html(block):
    children = []
    for line in block.split("\n"):
        line = line.lstrip("> ")
        children.extend(map(text_node_to_html_node, text_to_textnodes(line)))

    return ParentNode("blockquote", children)

def unordered_list_to_html(block):
    children = []
    for line in block.split("\n"):
        line = line.lstrip("* ").lstrip("- ")
        children.extend(map(text_node_to_html_node, text_to_textnodes(line)))

    for child in children:
        child.tag = 'li'
    return ParentNode("ul", children)

def ordered_list_to_html(block):
    children = []
    counter = 1
    for line in block.split("\n"):
        line = line.lstrip(f"{counter}. ")
        children.extend(map(text_node_to_html_node, text_to_textnodes(line)))
        counter += 1

    for child in children:
        child.tag = 'li'

    return ParentNode("ol", children)

def code_to_html(block):
    children = []
    block = block.strip('```').lstrip('```')
    for line in block.split("\n"):
        children.extend(map(text_node_to_html_node, text_to_textnodes(line)))

    return ParentNode("pre", [ParentNode("code", children)])

def heading_to_html(block):
    children = []
    start = find_starting_hashes(block)[0]
    n = len(start) - 1
    for line in block.split('\n'):
        line = block.lstrip(start)
        children.extend(map(text_node_to_html_node, text_to_textnodes(line)))

    return ParentNode(f"h{n}", children)

def paragraph_to_html(block):
    children = []
    children.extend(map(text_node_to_html_node, text_to_textnodes(block)))

    return ParentNode("p", children)

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == block_type_heading:
            children.append(heading_to_html(block))
        if type == block_type_quote:
            children.append(quote_to_html(block))
        if type == block_type_code:
            children.append(code_to_html(block))
        if type == block_type_unordered_list:
            children.append(unordered_list_to_html(block))
        if type == block_type_ordered_list:
            children.append(ordered_list_to_html(block))
        if type == block_type_paragraph:
            children.append(paragraph_to_html(block))


    return ParentNode('div', children, None)
