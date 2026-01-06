import re


def extract_title(markdown: str):
    title = re.search(r"(?<=^\#)([^\#\n]+)", markdown, re.MULTILINE)
    if title is None:
        raise ValueError("Title h1 not found in markdown text")
    return title.group().strip()
