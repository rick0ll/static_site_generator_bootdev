from copy import copy_static
from re import template
from generate_page import generate_pages_recursive
import os


def main():
    from_path = "content"
    dest_path = "public"
    template_path = "template.html"
    copy_static()
    generate_pages_recursive(from_path, template_path, dest_path)


main()
