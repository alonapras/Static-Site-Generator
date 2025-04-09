import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)

    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        for i in range(len(sections)): 
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        # for (index, section) in enumerate(sections):
        #     if not section:
        #         continue
        #     if index % 2 == 0:
        #         split_nodes.append(TextNode(sections, TextType.TEXT))
        #     else:
        #         split_nodes.append(TextNode(sections, text_type))

        new_nodes.extend(split_nodes)
    return new_nodes


# def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type is not TextType.TEXT:
#             new_nodes.append(node)
#         elif delimiter is None:
#             new_nodes.append(node)
#         else:
#             node_parts = node.text.split(delimiter)
#             for (index, part) in enumerate(node_parts):
#                 if not part:
#                     continue
#                 if index % 2 == 1:
#                     node = TextNode(part, text_type)
#                     new_nodes.append(node)
#                 else:
#                     node = TextNode(part, TextType.TEXT)
#                     new_nodes.append(node)
#     return new_nodes
    


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        extracted_images = extract_markdown_images(old_node.text)
        node_text = old_node.text
        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue

        for image in extracted_images:
            # the `maxsplit` argument (last argument of `split`) is the maximum times string splitted
            # it's only needed to avoid cases there node_text could contain two (or more) identical images
            sections = node_text.split(f"![{image[0]}]({image[1]})", 1)

            # this condition is not fulfilled
            # if len(sections) != 2:
            #     raise ValueError("invalid markdown, image section not closed")
            
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = sections[1]

        if len(node_text)>0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        extracted_links = extract_markdown_links(old_node.text)
        node_text = old_node.text
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue

        for link in extracted_links:
            # the `maxsplit` argument (last argument of `split`) is the maximum times string splitted
            # it's only needed to avoid cases there node_text could contain two (or more) identical images
            sections = node_text.split(f"[{link[0]}]({link[1]})", 1)

            # if len(sections) != 2:
            #     raise ValueError("invalid markdown, image section not closed")

            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = sections[1]

        if len(node_text)>0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

