import re
import os
import sys

# markdown_file
# source - path to source folder
# pattern - regular expression pattern for Markdown headers
def get_dictionary_structure_from_headers_content(markdown_file="", separator_list=['# ', '## ']):
    with open(markdown_file, 'r') as file:
        lines = file.readlines()

    data = {}
    current_section = None

    h1 = separator_list[0]
    h2 = separator_list[1]
    for line in lines:
        if line.startswith(h1):
            current_section = line.strip().replace(h1, "")
            data[current_section] = ""
        elif line.startswith(h2):
            current_section = line.strip().replace(h2, "")
            data[current_section] = ""
        elif current_section is not None:
            data[current_section] += line

    return data

from .get_url_list import get_url_list
from .get_header_list import get_header_list
