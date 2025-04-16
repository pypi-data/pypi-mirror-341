import os
import sys

sys.path.append('../')
import io
import shutil
import base64
from pdf2image import convert_from_path
from wand.image import Image
from io import BytesIO

from .convert_pdf_to_base64 import convert_pdf_to_base64
from .get_filename_from_path import get_filename_from_path
from .check_and_create_path import check_and_create_path
from ocr.get_company_from_pdf import get_company_from_pdf
from ocr.CompanyList import CompanyList
from ocr.get_date_from_pdf import get_date_from_pdf
from ocr.get_date_from_pdf_pattern import get_date_from_pdf_pattern
import json
import re


# pip3 install pdf2image wand pillow pdf2image

def sum_year_from_path_to_file(year, filename, extension, paths_dict, path_out="./"):
    if extension not in ['csv', 'txt', 'xls']:
        raise ValueError('Invalid extension! Accepted values: tar, zip')

    file_name = f'{filename}.{extension}'
    data_file_path = os.path.join(path_out, file_name)
    print(data_file_path)

    try:
        for path, file_out in paths_dict.items():
            if os.path.isdir(path):
                # tmp_path_out = os.path.join(path, file_out)
                print(path)
                dict_data = scan_recursive(path)
                json_path = f'./report/{year}.json'
                json.dump(dict_data, open(json_path, 'w'))

            else:
                print(f'{path} is not a directory. Skipping...')

        return f'Data file {data_file_path} created successfully!'

    except Exception as e:
        print(f'An error occurred while converting: {e}')





def scan_recursive(path, extension_list=['.pdf'], path_out="./report/2023/img/"):
    dict_list = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            for extension in extension_list:
                if filename.endswith(extension):
                    dict_data = {}

                    dict_data['filename'] = filename

                    print("filename:", filename)
                    file_path = os.path.join(root, filename)

                    print("file_path:", file_path)

                    # path of source file
                    pdf_path = os.path.join(path_out, f'{filename}.path')
                    #dict_data['path'] = 'file://' + file_path
                    dict_data['full_path'] = file_path

                    current_path = os.path.abspath(os.getcwd())
                    dict_data['year_path'] = file_path.replace(current_path, "")

                    words = file_path.split("expenses")
                    dict_data['month_path'] = words[1]

                    dict_data['folder_date'] = ""
                    match = re.search(r'/expenses/(\d{2}.\d{4})/', file_path)

                    if match:
                        result = match.group(1)
                        dict_data['folder_date'] = result

                    # with open(pdf_path, "w") as file:
                    #    file.write(file_path)

                    # icon of pdf
                    base64_icon = ""
                    base64_icon = convert_pdf_to_base64(file_path, path_out)
                    dict_data['image'] = base64_icon

                    # get price to file *.pdf.price

                    # get date to file *.pdf.date
                    invoice_company_list = get_company_from_pdf(
                        file_path,
                        [],
                        CompanyList().sorted_from_shortest_to_longest_name()
                    )
                    # print(invoice_company_list)

                    if len(invoice_company_list) > 0:
                        invoice_company = str(invoice_company_list[0])
                        # print("scan_recursive invoice_company: ", invoice_company)
                        dict_data['company'] = invoice_company
                        # pdf_path = os.path.join(path_out, f'{filename}.company')
                        # with open(pdf_path, "w") as file:
                        #    file.write(invoice_company)

                    invoice_date_list = []
                    try:
                        invoice_date_list = get_date_from_pdf(
                            file_path,
                            ['%d.%m.%Y'],
                            get_date_from_pdf_pattern.pattern_clean_list,
                            get_date_from_pdf_pattern.pattern_input_list
                        )
                    except Exception as e:
                        print(e)
                        #continue

                    if len(invoice_date_list) > 0:
                        invoice_date = str(invoice_date_list[0])
                        dict_data['date'] = invoice_date
                        # pdf_path = os.path.join(path_out, f'{filename}.date')
                        # with open(pdf_path, "w") as file:
                        #    file.write(invoice_date)

                    dict_list.append(dict_data)
                    print(dict_data)
                    #exit()

    # Sort JSON data by 'folder_date'
    dict_list_sorted = sorted(dict_list, key=lambda x: x['folder_date'])

    return dict_list_sorted
