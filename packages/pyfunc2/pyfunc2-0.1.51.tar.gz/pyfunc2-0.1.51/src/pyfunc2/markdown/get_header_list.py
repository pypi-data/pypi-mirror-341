import re
import os


def get_header_list(markdown, pattern=r'^#{1,6}\s+(.*)$'):
    # regex pattern to match all markdown headers
    header_list = re.findall(pattern, markdown, re.MULTILINE)
    #print(header_list)
    return header_list
