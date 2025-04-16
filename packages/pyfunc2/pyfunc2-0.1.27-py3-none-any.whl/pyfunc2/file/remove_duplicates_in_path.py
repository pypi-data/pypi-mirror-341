import sys

sys.path.append('../')

from file.find_duplicates import find_duplicates
from file.move_file import move_file


def remove_duplicates_in_path(source, duplicated):
    # Provide directory paths here

    duplicates = []
    not_duplicated = []

    compare_files = find_duplicates(source)
    source_files = find_duplicates(source)

    # Compare the hashes
    for file_hash, file_path in compare_files.items():
        if file_hash in source_files and file_path != source_files[file_hash]:
            duplicates.append((file_path, source_files[file_hash]))
            print("remove_duplicates duplicated:", file_path, source_files[file_hash])
            #move_file(file_path, '', duplicated)
            print()
            # exit()
        else:
            not_duplicated.append(file_path)
            #print("remove_duplicates not:", file_path)
    exit()

    # Print duplicate files
    for dup in duplicates:
        print(f'remove_duplicates duplicated: {dup[0]} = {dup[1]}')

    for file_path in not_duplicated:
        print("remove_duplicates not:", file_path)
