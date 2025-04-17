import os
import io
import base64
from pdf2image import convert_from_path
import sys

sys.path.append('../../')

def convert_pdf_to_base64(pdf_path, extension="png", dpi=70, path_out="./report/2023/img/"):
    from .check_and_create_path import check_and_create_path
    from .get_filename_from_path import get_filename_from_path
    check_and_create_path(path_out)
    images = convert_from_path(pdf_path, dpi, path_out, fmt=extension, single_file=True,
                               output_file=get_filename_from_path(pdf_path))

    print(images)
    img = images[0]
    in_mem_file = io.BytesIO()
    img.save(in_mem_file, format="PNG")
    # reset file pointer to start
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')

    return base64_encoded_result_str