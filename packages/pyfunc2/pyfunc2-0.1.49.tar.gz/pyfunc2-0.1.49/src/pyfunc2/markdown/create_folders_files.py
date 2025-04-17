import re
import os
import sys
import string

from .get_url_list import get_url_list
from .get_dictionary_structure_from_headers_content import get_dictionary_structure_from_headers_content
from .get_dictionary_structure_by_separator_list import get_dictionary_structure_by_separator_list
from .get_code_extension_dict import get_code_extension_dict


# markdown_file
# source - path to source folder
# pattern - regular expression pattern for Markdown headers
def create_folders_files(markdown_file="",
                         path="",
                         pattern_list=[r'^#{1,6}\s+(.*)$'],
                         extension_list=['bash', 'php', 'js', 'javascript', 'shell', 'sh'],
                         extension_head_list={
                             'bash': '#!/bin/bash',
                             'shell': '#!/bin/shell',
                             'sh': '#!/bin/sh',
                             'php': '<?php'
                         }
                         ):
    import re
    # Wczytaj plik markdown
    with open(markdown_file, 'r') as file:
        markdown = file.read()
    # Wyciągnij nagłówki
    headers = re.findall(pattern_list[0], markdown, re.MULTILINE)
    # Wyciągnij bloki kodu
    code_blocks = re.findall(r'```(\w+)?\n([\s\S]*?)```', markdown)
    for idx, header in enumerate(headers):
        if header:
            path_folder = os.path.join(path, header.strip())
            os.makedirs(path_folder, exist_ok=True)
            # Zapisz README.md z treścią sekcji (opcjonalnie)
            # path_file = os.path.join(path_folder, 'README.md')
            # with open(path_file, "w") as f:
            #     f.write(header)
            # Zapisz pliki kodów (jeśli są)
            if idx < len(code_blocks):
                lang, code = code_blocks[idx]
                extension = lang if lang else 'txt'
                filename = f"{idx+1}.{extension}"
                path_file = os.path.join(path_folder, filename)
                with open(path_file, "w") as f:
                    f.write(code.strip())
