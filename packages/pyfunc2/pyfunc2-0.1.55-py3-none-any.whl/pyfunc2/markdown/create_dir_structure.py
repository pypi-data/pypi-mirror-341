import os
import re

def create_dir_structure(md_text, base_dir):
    # Twórz katalog z każdej niepustej linii tekstu
    for line in md_text.splitlines():
        name = line.strip()
        if name:
            pathf = os.path.join(base_dir, name)
            os.makedirs(pathf, exist_ok=True)


def test(base_dir, filename):
    # Open and read markdown file
    with open(filename, "r") as md_file:
        md_text = md_file.read()

    create_dir_structure(md_text, base_dir)
