from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from markdown_to_blocks import markdown_to_blocks
from block_type import block_to_block_type, BlockType
from text_to_textnode import text_to_textnodes
from textnode import text_node_to_html_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    children = []

    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    
    return children

def heading_to_html_node(block):
    level = 0

    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    tag = f"h{level}"
    heading_text = block[level + 1:]
    heading_children = text_to_children(heading_text)
    heading_node = ParentNode(
        tag,
        heading_children,
    )

    return heading_node

def quote_to_html_node(block):
    quote_lines = []

    for line in block.split("\n"):
        quote_lines.append(line.lstrip(">").strip())

    quote_text = "\n".join(quote_lines)
    quote_children = text_to_children(quote_text)
    quote_node = ParentNode(
        "blockquote",
        quote_children,
    )

    return quote_node

def code_to_html_node(block):
    lines = block.strip().split("\n")
    code_text = "\n".join(lines[1:-1])
    code_node = ParentNode(
        "pre",
        [
            ParentNode(
                "code", 
                [LeafNode(None, code_text)],
            )
        ],
    )

    return code_node

def unordered_list_to_html_node(block):
    list_item_nodes = []

    for line in block.split("\n"):
        item_text = line[2:]

        unordered_list_children = text_to_children(item_text)

        li_node = ParentNode(
            "li",
            unordered_list_children,
        )
        list_item_nodes.append(li_node)

    unordered_list_node = ParentNode(
        "ul",
        list_item_nodes,
    )

    return unordered_list_node

def ordered_list_to_html_node(block):
    ordered_list_item_nodes = []

    for line in block.split("\n"):
        item_text = line.split(". ", 1)[1]

        ordered_list_children = text_to_children(item_text)

        li_node = ParentNode(
            "li",
            ordered_list_children,
        )
        ordered_list_item_nodes.append(li_node)

    ordered_list_node = ParentNode(
        "ol",
        ordered_list_item_nodes,
    )

    return ordered_list_node

def markdown_to_html_node(markdown:str) -> HTMLNode:

    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            block_node = ParentNode(
                "p",
                text_to_children(block),
            )

        elif block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)

        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)     

        elif block_type == BlockType.CODE:
            block_node = code_to_html_node(block)
        
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_list_to_html_node(block)

        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_to_html_node(block)

        else:
            raise ValueError(f"Unknown block type: {block_type}")

        children.append(block_node)
    
    return ParentNode("div", children)