# https://pypi.org/project/datefinder/
import re
from datetime import datetime
import locale

# Install:
# python -m pip install pdfreader
# python -m pip install datefinder

# format
# Extracting a date from a PDF invoice file involves several steps, namely 1) reading the PDF file, 2) extracting the text data from the file, and 3) searching the text for dates, which can appear in a variety of formats. In this case, we will be using the PyPDF2 module to read the PDF and the datefinder module to identify dates within the text.

import dateutil.parser as dparser

import sys
from pypdf import PdfReader


# pip3 install pypdf

def convertPdf2String(path):
    # load PDF file
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    return text


# https://dateutil.readthedocs.io/en/stable/parser.html
# pip install python-dateutil
def remove_extra_spaces(text):
    no_extra_spaces_text = ' '.join(text.split())
    return no_extra_spaces_text


def remove_all_spaces(text):
    no_spaces_text = text.replace(" ", "")
    return no_spaces_text


def remove_only_single_spaces(text):
    return re.sub(r'(?<=\S) (?=\S)', '', text)


def get_date_from_pdf(file_path,
                      format_out_list=['%Y'],
                      pattern_clean_list='[^A-Za-z0-9 .-]+',
                      pattern_input_list=[r'\d{2}\.\d{2}\.\d{4}'],
                      local_format_list=[]
                      ):
    if not len(local_format_list):
        # Get the default locale settings
        default_locale = locale.getlocale()[0]
        # Print the default locale settings for English
        # print('default_locale', default_locale)
        local_format_list.append(default_locale)

    fd = open(file_path, "rb")
    # viewer = SimplePDFViewer(fd)
    # viewer.render()
    # text = str(viewer.canvas.strings)

    # text = convertPdf2String(fd).encode("ascii", "xmlcharrefreplace")
    text = convertPdf2String(fd)
    # print(text)
    # text = ''.join(e for e in text if e.isalnum())
    for pattern_clean in pattern_clean_list:

        try:
            if pattern_clean == "remove_extra_spaces":
                text = remove_extra_spaces(text)
            elif pattern_clean == "remove_all_spaces":
                text = remove_all_spaces(text)
            elif pattern_clean == "remove_only_single_spaces":
                text = remove_only_single_spaces(text)
            else:
                text = re.sub(pattern_clean, '', text)

        except Exception as e:
            print("\nget_date_from_pdf exception: ", e)
            print("get_date_from_pdf pattern_clean_list: ", pattern_clean_list)
            print("get_date_from_pdf pattern_clean: ", pattern_clean)
            continue
        # text = re.sub('\W+', '', text)
        # print(text)

        # print(match)
        # date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        # dates = datetime.strptime(match.group(), '%Y').date()

        for pattern in pattern_input_list:

            data_pattern_list = []
            if len(pattern[1]):
                data_pattern_list = pattern[1]
            else:
                data_pattern_list.append(default_locale)

            matches = re.findall(pattern[0], text)
            # print("matches: ", matches, len(matches))
            if len(matches):
                out_by_format_list = []
                for match in matches:
                    for data_pattern in data_pattern_list:
                        # print(pattern, pattern[0])
                        # exit()
                        datestr = str(match)
                        # print('datestr', datestr)
                        # exit()
                        try:

                            # date_format='%b%d%Y'
                            if len(pattern) > 1:

                                if len(pattern) > 2:
                                    print(pattern[2])
                                    # Pierwsza część `(?<=\d)(st|nd|rd|th)\b` odpowiada za usuwanie 'st', 'nd', 'rd', 'th' po liczbie,
                                    # druga część `\s` odpowiada za usuwanie spacji. Operator `|` w wyrażeniu regularnym oznacza "lub", dzięki czemu wyrażenie pasuje do dowolnej z tych dwóch części.
                                    datestr = re.sub(data_pattern, '', datestr)
                                    dates = datetime.strptime(datestr, pattern[2])
                                else:
                                    print(data_pattern)
                                    dates = datetime.strptime(datestr, data_pattern)
                            else:
                                dates = dparser.parse(datestr, fuzzy=True)
                        # print('dates', dates)
                        except Exception as e:
                            print("\n !!!: ", e)
                            print("local_format_list", local_format_list)
                            print("out_by_format_list", out_by_format_list)
                            continue


                        # exit()
                        # print('local_format_list', local_format_list)
                        for local_format in local_format_list:
                            # Set the locale to German, ...
                            locale.setlocale(locale.LC_TIME, local_format)
                            # print('local_format', local_format)
                            for format_out in format_out_list:
                                out_by_format_list.append(
                                    dates.strftime(format_out)
                                )

                        print('out_by_format_list', out_by_format_list)
                        return out_by_format_list
    return []
    # print()
    # current_day = datetime.now().strftime('%Y')
    # dates = datetime.strptime(match.group(), '%Y').date()
    # print(dates)

    # for page_num in range(num_pages):
    #    page_obj = pdf_reader.getPage(page_num)
    #    text += page_obj.extractText()

    # matches = datefinder.find_dates(str(text))

    # for match in matches:
    #    print(match)
    # return match
