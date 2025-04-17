import datefinder
# https://pypi.org/project/datefinder/
import re
import numpy as np
from datetime import datetime
import sys
sys.path.append('../')
from .convert_pdf_to_string import convert_pdf_to_string
from ..text.remove_extra_spaces import remove_extra_spaces
from ..text.remove_all_spaces import remove_all_spaces
from ..text.remove_new_lines import remove_new_lines
from ..text.remove_only_single_spaces import remove_only_single_spaces
from ..text.multiple_search import multiple_search

# format
# Extracting a date from a PDF invoice file involves several steps, namely 1) reading the PDF file, 2) extracting the text data from the file, and 3) searching the text for dates, which can appear in a variety of formats. In this case, we will be using the PyPDF2 module to read the PDF and the datefinder module to identify dates within the text.

import dateutil.parser as dparser


def find_string_in_pdf(file_path, find_text="", find_text_list=[]):
    fd = open(file_path, "rb")

    # text = convertPdf2String(fd).encode("ascii", "xmlcharrefreplace")
    text = convert_pdf_to_string(fd)
    text = text.lower()
    text = remove_new_lines(text)

    find_text = find_text.lower()
    find_text_list = [find_text]

    # print("find_string_in_pdf find_text_list: ", find_text, find_text_list)

    # if len(find_text) > 2:
    #    find_text_list.append(find_text)

    if len(find_text_list) < 1:
        print("find_text_list empty")
        exit()

    text_list_out = multiple_search(text, find_text_list, [])

    if not text_list_out:
        text = remove_only_single_spaces(text)
        # print(text)
        text_list_out = multiple_search(text, find_text_list)

    # print("text_list_out: ", text_list_out)
    return text_list_out
    # return [file_path, text_list_out]
