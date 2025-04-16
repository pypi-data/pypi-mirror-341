import sys
sys.path.append('../')

from .find_duplicates import find_duplicates
from .move_file import move_file

#  Python script to find duplicate files between two different directories by comparing their hash values. This script assumes that files with the same content will have the same hash value.

def remove_duplicates(source, compare, duplicated):
    # Provide directory paths here

    duplicates = []
    not_duplicated = []

    compare_files = find_duplicates(compare)
    source_files = find_duplicates(source)

    # Compare the hashes
    for file_hash, file_path in compare_files.items():
        if file_hash in source_files:
            duplicates.append((file_path, source_files[file_hash]))
            print("remove_duplicates duplicated:", file_path, source_files[file_hash])
            move_file(file_path, '', duplicated)
            print()
            # exit()
        else:
            not_duplicated.append(file_path)
            # print("remove_duplicates not:", file_path)

    # Print duplicate files
    for dup in duplicates:
        print(f'remove_duplicates duplicated: {dup[0]} = {dup[1]}')

    for file_path in not_duplicated:
        print("remove_duplicates not:", file_path)
