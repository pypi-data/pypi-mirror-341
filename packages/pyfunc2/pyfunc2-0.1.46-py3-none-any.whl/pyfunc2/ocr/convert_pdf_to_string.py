import PyPDF2
import sys
from pypdf import PdfReader

from pdfreader import SimplePDFViewer
# python -m pip install pdfreader

# Install:
# pip3 install pypdf
# python -m pip install pdfreader
# python -m pip install datefinder

def convert_pdf_to_string(path):
    # load PDF file
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    return text


