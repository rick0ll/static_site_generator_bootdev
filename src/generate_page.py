from re import template
from markdown_to_html import markdown_to_html_node
from extract_title import extract_title
import os


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise OSError("Path con contenuto website mancante " + dir_path_content)

    content_list = os.listdir(dir_path_content)
    for content in content_list:
        content_path = os.path.join(dir_path_content, content)
        if os.path.isfile(content_path):
            dest_path = os.path.join(dest_dir_path, content)
            dest_path = dest_path.replace(".md", ".html")
            generate_page(content_path, template_path, dest_path)
        else:
            new_dir_path = os.path.join(dest_dir_path, content)
            generate_pages_recursive(content_path, template_path, new_dir_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        file_content = file.read()

    with open(template_path) as file:
        template_content = file.read()

    html_file = markdown_to_html_node(file_content).to_html()
    title = extract_title(file_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_file)

    dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(dest_path, "w") as file:
        file.write(template_content)
