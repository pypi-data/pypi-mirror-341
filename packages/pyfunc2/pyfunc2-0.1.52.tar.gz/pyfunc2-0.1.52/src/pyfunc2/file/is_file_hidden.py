import os


def is_file_hidden(filepath):
    filename = os.path.basename(filepath)
    return filename.startswith('.')
