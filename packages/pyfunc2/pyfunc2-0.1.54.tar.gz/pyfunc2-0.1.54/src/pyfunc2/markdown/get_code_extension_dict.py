import re
import os
import sys
import string

from .get_url_list import get_url_list
from .get_dictionary_structure_from_headers_content import get_dictionary_structure_from_headers_content
from .get_dictionary_structure_by_separator_list import get_dictionary_structure_by_separator_list


def get_code_extension_dict(
        content,
        extension_list=['bash', 'php', 'js', 'javascript', 'shell', 'sh', 'python'],
        extension_head_list={
            'bash': '#!/bin/bash',
            'shell': '#!/bin/shell',
            'sh': '#!/bin/sh',
            'php': '<?php',
            'python': '#!/bin/python'
        },
        result_list=[]
):
    code_blocks = get_dictionary_structure_by_separator_list(content)

    for i, block in enumerate(code_blocks, 1):
        # print(f"Code Block {i}:\n{block}\n")
        extension = "txt"
        result = block
        # if block.splitlines(True)[0]:
        first_line = block.splitlines(True)[0]
        first_line = first_line.replace('\n', '')
        filename = str(i)
        if len(first_line) >= 1:
            # result = ""
            code_list = first_line.split(' ')
            # print(code_list)
            if len(code_list) >= 1:
                language = re.sub('[^A-Za-z0-9]+', '', first_line)
                # print(first_line)
                # print(language)
                # print(block)
                # exit()
                if language in extension_list:
                    extension = language
                    # print(first_line.split(language))
                    # exit()
                    # continue

                    # first line second part is filename, if not empty save to variable
                    if (len(first_line) > len(language)) and (len(first_line.split(language)) > 0) and (
                            first_line.split(language)[1]):
                        filename = first_line.split(language)[1]

                    post = block.split("\n", 1)[1]
                    if extension in extension_head_list.keys():
                        result = extension_head_list[language] + '\n'

                    result = result + post

        result_list.append({'extension': extension, 'code': result, 'filename': filename})

    return result_list
