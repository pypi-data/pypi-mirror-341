import re
import os
import sys

# markdown_file
# source - path to source folder
# pattern - regular expression pattern for Markdown headers
def create_dir_structure_from_headers(markdown_file="", path="", pattern_list=[r'^#{1,6}\s+(.*)$']):
    import re
    with open(markdown_file, 'r') as file:
        markdown = file.read()
    # Wyciągnij wszystkie nagłówki (tylko tekst, bez #)
    headers = re.findall(pattern_list[0], markdown, re.MULTILINE)
    for header in headers:
        if header:
            path_folder = os.path.join(path, header.strip())
            os.makedirs(path_folder, exist_ok=True)



from .get_url_list import get_url_list
from .get_header_list import get_header_list
