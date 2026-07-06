from textnode import TextNode, TextType
from markdown_extractors import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: TextType,
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown: missing closing delimiter {delimiter}")
        
        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
                
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        extract = extract_markdown_images(old_node.text)
        
        if not extract:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for image_alt, image_link in extract:
            markdown_image = f"![{image_alt}]({image_link})"
            parts = remaining_text.split(markdown_image, 1)

            before = parts[0]
            after = parts[1]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            remaining_text = after
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        extract = extract_markdown_links(old_node.text)

        if not extract:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for link_text, link_url in extract:
            markdown_link = f"[{link_text}]({link_url})"
            parts = remaining_text.split(markdown_link, 1)

            before = parts[0]
            after = parts[1]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            remaining_text = after
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes