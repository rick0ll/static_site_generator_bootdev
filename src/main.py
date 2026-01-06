from copy import copy_static
from re import template
from generate_page import generate_pages_recursive
import os
import sys


def main():
    base_path = "/"
    if len(sys.argv) >= 2:
        base_path = sys.argv[1]

    from_path = "content"
    dest_path = "docs"
    template_path = "template.html"
    copy_static()
    generate_pages_recursive(from_path, template_path, dest_path, base_path)


main()
