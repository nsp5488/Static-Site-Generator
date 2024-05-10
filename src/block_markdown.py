block_type_paragraph = 'paragraph'
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
import re

def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    out = []
    block = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
           block.append(line)
        else:
            out.append("\n".join(block))
            block = []
    out.append(block)
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
    can_be_quote = True
    can_be_ul = True
    can_be_ol = True
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
            can_be_ul
    if can_be_quote:
        return block_type_quote
    if can_be_ul:
        return block_type_unordered_list
    if can_be_ol:
        return block_type_ordered_list
    
    return block_type_paragraph