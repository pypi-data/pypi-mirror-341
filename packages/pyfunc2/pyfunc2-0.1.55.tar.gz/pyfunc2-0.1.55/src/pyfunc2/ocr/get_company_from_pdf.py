# import PyPDF2
# python -m pip install pdfreader
# https://pypi.org/project/datefinder/
import re
from pypdf import PdfReader

# Install:
# python -m pip install pdfreader
# python -m pip install datefinder
# format
# Extracting a date from a PDF invoice file involves several steps, namely 1) reading the PDF file, 2) extracting the text data from the file, and 3) searching the text for dates, which can appear in a variety of formats. In this case, we will be using the PyPDF2 module to read the PDF and the datefinder module to identify dates within the text.


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


def get_company_from_pdf(file_path,
                         pattern_clean_list='[^A-Za-z0-9 .-]+',
                         company_list=[""]):
    fd = open(file_path, "rb")
    # viewer = SimplePDFViewer(fd)
    # viewer.render()
    # text = str(viewer.canvas.strings)

    # text = convertPdf2String(fd).encode("ascii", "xmlcharrefreplace")
    text = convertPdf2String(fd)
    text = text.lower()
    # print(text)

    # text = ''.join(e for e in text if e.isalnum())
    if pattern_clean_list:
        for pattern_clean in pattern_clean_list:
            if pattern_clean == "remove_extra_spaces":
                text = remove_extra_spaces(text)
            elif pattern_clean == "remove_all_spaces":
                text = remove_all_spaces(text)
            elif pattern_clean == "remove_only_single_spaces":
                text = remove_only_single_spaces(text)
            else:
                text = re.sub(pattern_clean, '', text)
            # text = re.sub('\W+', '', text)
            text = text.replace(' ', '_')

    #print(text)
    # exit()
    # sortowanie firm od najdluzszej nazwy

    company_list_out = find_company(text, company_list, [])

    if not company_list_out:
        text = remove_only_single_spaces(text)
        #print(text)
        company_list_out = find_company(text, company_list)

    #print("company_list_out: ", company_list_out)

    #exit()

    return company_list_out


def find_company(text="", company_list=[], company_list_out=[]):
    company_occ_list = {}
    for company in company_list:

        matches = text.find(company)
        #print(company, matches, len(text))
        if matches >= 0:
            #company_list_out.append(company)
            print(company, matches, len(text))
            company_occ_list[company] = matches

    sorted(company_occ_list)
    #print("company_occ_list: ", company_occ_list)
    company_list_out = list(company_occ_list.keys())
    #print("company_list_out: ", company_list_out)
    return company_list_out


