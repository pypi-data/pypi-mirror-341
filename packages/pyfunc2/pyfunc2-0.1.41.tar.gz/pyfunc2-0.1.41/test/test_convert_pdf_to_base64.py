import os
import io
import tempfile
import base64
import pytest
from pyfunc2.file.convert_pdf_to_base64 import convert_pdf_to_base64
from PIL import Image
from fpdf import FPDF

def create_sample_pdf(path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test PDF", ln=True, align='C')
    pdf.output(path)

def test_convert_pdf_to_base64_png_and_jpeg():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "test.pdf")
        create_sample_pdf(pdf_path)
        # Test PNG
        b64_png = convert_pdf_to_base64(pdf_path, extension="png")
        img_bytes = base64.b64decode(b64_png)
        img = Image.open(io.BytesIO(img_bytes))
        assert img.format == "PNG"
        # Test JPEG
        b64_jpeg = convert_pdf_to_base64(pdf_path, extension="jpeg")
        img_bytes_jpeg = base64.b64decode(b64_jpeg)
        img_jpeg = Image.open(io.BytesIO(img_bytes_jpeg))
        assert img_jpeg.format == "JPEG"
        # Test JPG alias
        b64_jpg = convert_pdf_to_base64(pdf_path, extension="jpg")
        img_bytes_jpg = base64.b64decode(b64_jpg)
        img_jpg = Image.open(io.BytesIO(img_bytes_jpg))
        assert img_jpg.format == "JPEG"

def test_convert_pdf_to_base64_invalid_file():
    with pytest.raises(Exception):
        convert_pdf_to_base64("not_a_pdf.pdf")
