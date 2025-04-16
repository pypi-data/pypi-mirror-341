import os
import sys

sys.path.append('../')

from .get_hash import get_hash


def find_duplicates(directory):
    """
    This function finds and returns duplicate files in the given directory
    """
    file_dict = {}
    for dir_path, dir_names, file_names in os.walk(directory):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            file_hash = get_hash(file_path)
            if file_hash not in file_dict:
                file_dict[file_hash] = file_path
                # print(file_hash, file_path)
                # move_file(file_path, '', duplicated)
                # exit()
    return file_dict
