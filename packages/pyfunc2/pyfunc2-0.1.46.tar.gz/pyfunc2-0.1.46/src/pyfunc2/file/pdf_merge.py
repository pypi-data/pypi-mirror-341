## https://chatgpt-static.s3.amazonaws.com/chats/uf98915.html

## In this script, the merge_pdfs function takes in the paths for the "cover" and "draft" folders as inputs, as well as the path for the "output" folder. It then iterates through the PDFs in both folders and match the files based on their numeric key (e.g. "1.pdf" from the cover folder with "1 - Letter of Approval.pdf" from the draft folder). And it Merges the matching files in the order of cover PDF first and draft PDF second, and all following pages. And finally saves the merged PDFs to the new "output" folder.
## You need to install PyPDF2 library to use this function.
## You can install by pip install PyPDF2
## Please note that this script is a basic example and is not production-ready. It is always recommended to thoroughly test and make necessary modifications for any specific requirements.


import os
from PyPDF2 import PdfMerger

# python -m pip install --upgrade pip
# pip install PyPDF2
# https://pypi.org/project/PyPDF2/

output_folder = ""
cover_folder = ""
draft_folder = ""


def merge_pdfs(cover_folder, draft_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

        # Get a list of PDFs in the cover and draft folders
        cover_pdfs = [f for f in os.listdir(cover_folder) if f.endswith('.pdf')]
        draft_pdfs = [f for f in os.listdir(draft_folder) if f.endswith('.pdf')]

        # Iterate through the cover PDFs
        for pdf in cover_pdfs:
            # Get the numeric key of the PDF
            key = pdf.split('.')[0]

            # Find the matching draft PDF with the same key
            matching_draft = [f for f in draft_pdfs if key in f][0]

            # Create a PdfMerger object
            merger = PdfMerger()

            # Add the cover and draft PDFs to the merger
            merger.append(f'{cover_folder}/{pdf}')
            merger.append(f'{draft_folder}/{matching_draft}')

            # Write the merged PDF to the output folder
            merger.write(f'{output_folder}/{matching_draft}')

        print(f'Merged {len(cover_pdfs)} PDFs to {output_folder}')

# Example usage
# merge_pdfs('cover', 'draft', 'output')
