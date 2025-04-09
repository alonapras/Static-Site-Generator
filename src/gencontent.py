import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath=None):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")

    with open(from_path, 'r') as content_file:
        markdown_content = content_file.read()
    # from_file = open(from_path, "r")
    # markdown_content = from_file.read()
    # from_file.close()

    with open(template_path, 'r') as template_file:
        template = template_file.read()
    # template_file = open(template_path, "r")
    # template = template_file.read()
    # template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)

    if basepath is not None:
        template = template.replace('href="/', f'href="{basepath}')
        template = template.replace('src="/', f'src="{basepath}')


    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, 'w') as output_file:
        output_file.write(template)
    # to_file = open(dest_path, "w")
    # to_file.write(template)


def extract_title(markdown):
    """
    It should pull the h1 header from the markdown file (the line that starts with a single #) and return it.
    If there is no h1 header, raise an exception.
    """
    #blocks = markdown_to_blocks(markdown)

    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            return line[2:].strip()
    raise ValueError("no title found")

"""
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    '''
    Generate pages recursively from the content directory to the public directory.
    '''
    for root, dirs, files in os.walk(dir_path_content):  
    # os.walk returns a generator, that creates a tuple of values (current_path, directories in current_path, files in current_path).
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir_path, os.path.relpath(from_path, dir_path_content)).replace(".md", ".html")
                generate_page(from_path, template_path, dest_path)

"""
# os.listdir
# os.path.join
# os.path.isfile
# pathlib.Path

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath=None):
    """
    Generate pages recursively from the content directory to the public directory.
    """
    os.makedirs(dest_dir_path, exist_ok=True)

    for item_name in os.listdir(dir_path_content):
        source_item_path = os.path.join(dir_path_content, item_name)
        dest_item_path = os.path.join(dest_dir_path, item_name) # Corresponding path in destination

        if os.path.isdir(source_item_path):
            generate_pages_recursive(source_item_path, template_path, dest_item_path)

        elif os.path.isfile(source_item_path):
            if source_item_path.endswith(".md"):
                dest_html_path = dest_item_path.replace(".md", ".html")
                # Or using pathlib (more robust):
                # dest_html_path = str(Path(dest_item_path).with_suffix(".html"))

            generate_page(
                from_path=source_item_path,  
                template_path=template_path,
                dest_path=dest_html_path,
                basepath=basepath
            )
