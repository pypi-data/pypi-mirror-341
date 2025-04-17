import os
import io
import base64
from PIL import Image
from pdf2image import convert_from_path  # pdf2image uses poppler

# Uwaga: pdf2image wymaga zainstalowanego poppler (system dependency)
# Nowoczesny kod: obsługuje tylko pierwszą stronę, PNG/JPEG, bez zapisu na dysk

def convert_pdf_to_base64(pdf_path, extension="png", dpi=100):
    """
    Konwertuje pierwszą stronę PDF do base64 (PNG/JPEG) bezpośrednio z pamięci.
    Wymaga: pip install pdf2image pillow
    """
    # Konwertuj PDF do listy obrazów (każda strona jako osobny obraz)
    images = convert_from_path(pdf_path, dpi=dpi, fmt=extension, single_file=True)
    if not images:
        raise ValueError("Nie udało się przekonwertować PDF na obraz.")
    img = images[0]
    in_mem_file = io.BytesIO()
    # Wybierz format na podstawie extension
    fmt = extension.upper()
    if fmt == "JPG":
        fmt = "JPEG"
    img.save(in_mem_file, format=fmt)
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()
    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
    return base64_encoded_result_str