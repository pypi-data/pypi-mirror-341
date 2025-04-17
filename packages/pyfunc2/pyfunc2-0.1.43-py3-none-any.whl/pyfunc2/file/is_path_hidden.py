import os
import sys

sys.path.append('../')

from .is_file_hidden import is_file_hidden


def is_path_hidden(filepath):
    filepath = filepath.replace('./', '')
    path_parts = filepath.split(os.sep)
    # print(path_parts)
    current_path = "/"
    for part in path_parts:
        if part:  # ignore if empty
            # print(part)
            if part.startswith('__') and part.endswith('__'):
                return True
            if part.startswith('.'):
                return True
            current_path = os.path.join(current_path, part)
            if is_file_hidden(current_path):
                return True
    return False
