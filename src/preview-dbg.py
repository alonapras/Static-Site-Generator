import re
text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some text"
pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

extracted_images = re.findall(pattern, text)

node_text = text
for image in extracted_images:
    sections = node_text.split(f"![{image[0]}]({image[1]})", 1)

    #new_nodes.append(TextNode(sections[0], TextType.TEXT))
    #new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
    print(sections, image)
    node_text = sections[1]


if len(node_text)>0:
    print(node_text)
